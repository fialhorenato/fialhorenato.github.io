---
title: "One Load per Key: Collapsing Duplicate Lookups with Spring Boot’s Cache and Caffeine"
description: "Use Spring’s cache abstraction and Caffeine’s atomic per-key loading to collapse concurrent duplicate lookups, with notes on empty values, metrics, eviction, and testing."
date: 2026-10-23
layout: single
tags:
  - Software Development
source_url: https://dev.to/fialhorenato/one-load-per-key-collapsing-duplicate-lookups-with-spring-boots-cache-and-caffeine-390p
---

Rule engines, aggregators, and validation pipelines share a hidden cost: independent components ask the same downstream question with the same key at the same time. Each component is correct on its own; together, they multiply the load on the system behind them.

This article shows how to collapse those calls into one load using Spring’s cache abstraction backed by Caffeine. It also covers details that can surprise you: cached empty results, metrics that change meaning, and tests that pass for the wrong reason.

## The scenario

Imagine a promotion eligibility service that evaluates about 20 rules in parallel: the product is in stock, its price is above a threshold, the seller is in good standing, its category is allowed, and so on.

~~~java
List<CompletableFuture<Boolean>> results = rules.stream()
        .map(rule -> CompletableFuture.supplyAsync(
                () -> rule.test(productId), executor))
        .toList();
~~~

Each rule depends on a small, focused service:

~~~java
@Component
class InStockRule implements Rule {
    private final StockService stockService;

    @Override
    public boolean test(String productId) {
        return stockService.isInStock(productId);
    }
}

@Service
class StockService {
    private final ProductCatalogue catalogue;

    boolean isInStock(String productId) {
        return catalogue.findProduct(productId)
                .map(product -> product.stock() > 0)
                .orElse(false);
    }
}
~~~

Pricing, seller, and category rules look similar. They read different fields from the same product, which comes from one place:

~~~java
@Service
public class ProductCatalogue {
    // Reads from a shared cache (Redis, DynamoDB, ...),
    // then falls back to the catalogue API on a miss.
    public Optional<Product> findProduct(String productId) {
        return store.get(productId).or(() -> fetchAndStore(productId));
    }
}
~~~

One evaluation can call findProduct about 20 times. On a warm path, that means 20 shared-cache reads and 20 deserializations of the same object. On a cold path, all 20 calls can miss together and send 20 concurrent requests to the catalogue API. That’s a cache stampede, and it tends to hit hardest when the downstream system is already struggling.

The callers don’t need 20 answers. They need one.

## Why not use request scope?

A request-scoped cache can memoize a response for the lifetime of an HTTP request, but it is not always a good fit:

- **Work can move between threads.** The rules run on executor threads, while request attributes are bound to the request thread. You would need to propagate that context to every executor, for example with a TaskDecorator.
- **Not all work comes from a request.** Queue consumers, Kafka listeners, and scheduled jobs have no HTTP request. A RequestScope bean there can fail with “No thread-bound request found.”

A short-lived in-process cache provides the same behavior across entry points. Its tradeoff is bounded staleness, which can be negligible with a short TTL.

## Set up Spring Cache and Caffeine

`spring-boot-starter-cache` provides Spring’s cache abstraction, but not Caffeine. Add both dependencies; Spring Boot manages the Caffeine version when its dependency management is in use.

Maven:

~~~xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
</dependency>
~~~

Gradle Kotlin DSL:

~~~kotlin
implementation("org.springframework.boot:spring-boot-starter-cache")
implementation("com.github.ben-manes.caffeine:caffeine")
~~~

Enable caching:

~~~java
@SpringBootApplication
@EnableCaching
public class Application { }
~~~

Then configure a bounded cache:

~~~yaml
spring:
  cache:
    type: caffeine
    cache-names: products
    caffeine:
      spec: maximumSize=10000,expireAfterWrite=30s,recordStats
~~~

Each setting matters:

- **type: caffeine** selects Caffeine explicitly. Without it, Spring Boot may choose a different cache provider, such as `ConcurrentMapCacheManager`, which does not apply Caffeine’s `spec`. Verify the active cache manager in the configuration used by your application.
- **cache-names** creates the named caches at startup and disables dynamic cache creation. A Cacheable annotation that refers to a name not listed here will fail at runtime. Predeclared caches also let Spring Boot bind Micrometer metrics to them.
- **spec** caps the entry count with maximumSize, limits staleness with expireAfterWrite, and enables hit and miss statistics with recordStats.

## Collapse concurrent misses

Apply Cacheable to the method that loads the product:

~~~java
@Cacheable(cacheNames = "products", key = "#productId", sync = true)
public Optional<Product> findProduct(String productId) {
    return store.get(productId).or(() -> fetchAndStore(productId));
}
~~~

sync = true is what changes caching into request collapsing. Without it, Spring checks the cache, sees a miss, calls the method, and stores the result. If 20 threads miss together, all 20 can call the method.

With sync = true, Spring asks the cache provider to load the key atomically. Caffeine uses a per-key computation: the first thread performs the load and the others wait for its result.

key = "#productId" makes the cache key explicit. For a one-argument method, Spring’s default key generator uses that argument. If a second parameter is later added, the default key changes shape, and a matching CacheEvict may stop evicting the intended entry. Referencing a parameter by name requires the -parameters compiler flag; otherwise, use #p0.

Evict one product:

~~~java
@CacheEvict(cacheNames = "products", key = "#productId")
public void evict(String productId) { }
~~~

Clear the whole cache:

~~~java
@CacheEvict(cacheNames = "products", allEntries = true)
public void evictAll() { }
~~~

A classic mistake is using CacheEvict("products") on a method with no arguments. It tries to evict the key SimpleKey.EMPTY, which clears nothing. Use allEntries = true to clear every entry.

## Details to decide deliberately

### Empty results are cached too

Spring unwraps Optional: present values are cached as values, while empty ones are represented as null. CaffeineCacheManager allows null values by default, so “product not found” is cached for the full TTL.

That may be what you want; without it, every caller can look up the same missing product again. But decide deliberately. The common escape hatch, unless = "#result == null", cannot be combined with sync = true. If empty results must not be cached, consider throwing a not-found exception (exceptions are not cached) or using the Cache API directly.

### Failures are not shared

Exceptions are not cached, which prevents a transient failure from sticking around for 30 seconds. But when a load fails, waiting callers do not receive one shared cached error; they can retry the load one after another. Under a sustained outage, put a circuit breaker or a stale-fallback strategy inside the loaded method. Don’t rely on the cache to absorb failures.

### Callers receive the same object instance

Before caching, each caller may have received a separately deserialized object. Now callers within the TTL share one object across threads. If a component mutates it, other components can observe that change unexpectedly.

Prefer immutable types, such as records or immutable generated classes. If that is not possible, document that the cached method returns a shared mutable object.

### Self-invocation bypasses the cache

Cacheable works through a Spring proxy. A call from inside the same class, such as this.findProduct(...), skips the proxy and therefore skips the cache. Confirm that each hot caller goes through the Spring bean.

### The cache is local to each instance

Each pod or application instance has its own cache. An eviction endpoint only clears the instance that receives the request; other instances can keep serving the old value until its TTL expires. That may be fine when the TTL is short, but document it for whoever operates the service.

### Existing metrics change meaning

Counters inside the cached method—shared-cache misses, remote calls, or fallbacks—now increment only on in-memory cache misses. After deployment, dashboards may show a sudden drop that looks like an outage or a miracle. It is neither. Tell dashboard owners before the change, and add the cache metrics exposed by recordStats:

- cache.gets{cache="products", result="hit"|"miss"}
- cache.puts
- cache.evictions
- cache.size

### Choose the TTL for the unit of work

The goal is to collapse calls within one unit of work, not necessarily to build a long-lived performance cache. The TTL should cover one evaluation, including slow paths such as retries and backoff, while keeping extra staleness negligible compared with the data’s normal freshness.

Seconds to tens of seconds is often a reasonable starting point. A longer TTL is a different cache design and needs its own invalidation strategy.

### Virtual threads on JDK 21–23

With `sync = true`, the load runs inside Caffeine’s atomic computation, which uses synchronization. On JDK 21–23, a virtual thread blocked on I/O while holding a monitor can pin its carrier thread. Many concurrent cold loads may therefore limit scheduler throughput on those JDK versions.

JDK 24 changed monitor handling in [JEP 491](https://openjdk.org/jeps/491). On older JDKs, load-test the cold path and use `-Djdk.tracePinnedThreads=full` to investigate pinning.

## Test that the calls really collapse

A naive test fires 20 calls and checks that the loader ran once. It can pass even without sync = true: if the stub returns immediately, calls may run one after another, and the first fills the cache before the next arrives.

Keep callers inside the loader until they have all arrived:

~~~java
@SpringJUnitConfig(ProductCatalogueCachingTest.Config.class)
class ProductCatalogueCachingTest {
    private static final int CALLERS = 20;

    @Autowired
    ProductCatalogue catalogue;

    @MockitoBean
    ProductStore store;

    @Test
    void concurrentMissesLoadOnce() throws Exception {
        var allCallersLoading = new CountDownLatch(CALLERS);
        var release = new CountDownLatch(1);

        when(store.get("p-1")).thenAnswer(invocation -> {
            allCallersLoading.countDown();
            release.await(5, TimeUnit.SECONDS);
            return Optional.of(new Product("p-1", 3));
        });

        try (var executor = Executors.newFixedThreadPool(CALLERS)) {
            var futures = IntStream.range(0, CALLERS)
                    .mapToObj(i -> executor.submit(
                            () -> catalogue.findProduct("p-1")))
                    .toList();

            allCallersLoading.await(500, TimeUnit.MILLISECONDS);
            release.countDown();

            for (var future : futures) {
                assertThat(future.get(5, TimeUnit.SECONDS)).isPresent();
            }
        }

        verify(store, times(1)).get("p-1");
    }

    @Configuration
    @EnableCaching
    static class Config {
        @Bean
        CacheManager cacheManager() {
            return new CaffeineCacheManager("products");
        }

        @Bean
        ProductCatalogue catalogue(ProductStore store) {
            return new ProductCatalogue(store);
        }
    }
}
~~~

With sync = true, the first caller enters the loader and the other 19 wait in Caffeine, so store.get runs once. Remove sync = true and the test should fail with 20 calls. A test you have never seen fail has not yet proved the behavior.

The test above builds its own CaffeineCacheManager, so it does not exercise application.yml. Add a separate configuration test that loads the real application configuration and verifies the cache type, name, maximum size, and expiry. Also test eviction and whichever empty-result behavior you choose.

## A practical checklist

- Declare spring-boot-starter-cache and Caffeine, and enable caching.
- Set spring.cache.type: caffeine so a missing dependency fails at startup.
- Declare cache names and keep them in sync with annotations.
- Set maximumSize, expireAfterWrite, and recordStats.
- Use Cacheable(sync = true) with an explicit key.
- Make CacheEvict use the same key; use allEntries = true to clear all entries.
- Decide whether to cache empty results and test that behavior.
- Return immutable cached values, or document that callers share an instance.
- Avoid self-invocation on hot paths.
- Warn dashboard owners that counters inside the cached method will change meaning.
- Write a concurrency test that fails without sync = true.
- Test the real cache configuration, not only a test-specific cache manager.
- On JDK 21–23 with virtual threads, load-test for pinning on the cold path.

The code change is small: a dependency, a few lines of YAML, and one annotation. Most of the value lies in the decisions around it: what gets cached (including “not found”), how configuration fails loudly instead of silently degrading, how metrics are interpreted, and whether tests actually fail when the behavior breaks.

Get those details right, and 20 components asking the same question can cost about the same as one.

Originally published on [DEV Community](https://dev.to/fialhorenato/one-load-per-key-collapsing-duplicate-lookups-with-spring-boots-cache-and-caffeine-390p).
