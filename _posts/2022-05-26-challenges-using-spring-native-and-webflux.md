---
title: "Spring Native and WebFlux: What I Learned from a PostgreSQL App"
tags:
  - Software Development
description: "A historical account of testing Spring Native, WebFlux, and R2DBC with PostgreSQL, including native-image build, persistence, and observability trade-offs."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
---

This is a report from a 2022 experiment with Spring Native, WebFlux, and R2DBC in a small news aggregation project. Spring Native was an experimental project that preceded the native-image support now integrated with Spring Boot 3. For a current project, start with the [Spring Boot native image documentation](https://docs.spring.io/spring-boot/reference/packaging/native-image/index.html); the limitations below describe the earlier stack and should be read as historical observations.

In my spare time, I created a pet project that aggregates news from several sources and delivers them to an Android app built with Flutter. The backend initially used:

```
Kotlin
Gradle KTS
Spring Boot (Data, MVC, Security, Actuator)
PostgreSQL (Liquibase for migrations)
Deployed on a heroku free tier dyno (Validating the idea)
```

At the time, I deployed the MVP on Heroku’s free tier while validating the idea. Heroku later discontinued its free dynos, so this deployment detail is historical.

The MVP was deployed on Heroku using a Gradle buildpack. I noticed two limitations: response times increased while importing content, and the dyno could sleep during idle periods, making the next startup slow (around 14 seconds in my observation).

I was concerned about response times and startup delay, so I explored Spring WebFlux and R2DBC. I wanted to learn whether the reactive stack could help this workload, while recognizing that it would add complexity and would not automatically remove the need to scale infrastructure.

I often use side projects to learn new technologies. This project helped me practice Kotlin and learn Dart and Flutter. At the time, I was unsure whether Spring Native and WebFlux were a good fit for the application, which had more than 500 monthly active users.

After attending WeAreDevelopers World Congress in Berlin in 2022, where Spring Native and WebFlux appeared in several talks, I tried the stack and recorded the issues I encountered:

## First mistakes

In hindsight, my first mistake was adopting both technologies at once. When something failed, I could not tell whether the cause was WebFlux, Spring Native, or my application code. Introducing one major change at a time would have made the experiment easier to diagnose.

The following sections describe what I observed in that experiment; they are not a complete list of current framework limitations.

### Native-image builds added deployment work

In 2022, producing a GraalVM native image required a build pipeline that could handle the ahead-of-time compilation and its resource needs. I used Spring Boot buildpacks via `./gradlew bootBuildImage` and deployed the resulting image using the platform’s container workflow. Platform support and command syntax change; check the current provider and Spring Boot documentation rather than treating these historical commands as current instructions.


### R2DBC required different persistence patterns

WebFlux does not require R2DBC, but blocking JDBC calls can undermine an end-to-end reactive request path. R2DBC offers non-blocking database access, with a different programming model from JPA. In the Spring Data R2DBC version I used, JPA-style relationship mapping such as `@OneToMany` and `@ManyToOne` was not available; data modeling and queries needed to account for that. APIs and capabilities have evolved, so check the current reference for your version.

### Liquibase needed native-image configuration

I initially tried to reuse code from another project that was already running successfully.

And the database migration management tool that I was using is Liquibase (Wasn't a must, but instead, a good to have tool).

In this 2022 experiment, Liquibase needed additional work to build into the native image. Native-image compatibility depends on the Liquibase and Spring versions and runtime features used. Check current Liquibase documentation and its [native-image issue history](https://github.com/liquibase/liquibase/issues/1552) before drawing conclusions for a new application.

### Observability agent compatibility required checking

Observability was another gap in my setup: the New Relic Java agent I used did not work with that native-image build. Actuator and Micrometer metrics remained options, but instrumentation support depends on the agent, framework, and native-image configuration. Verify compatibility with your current observability stack.

### Native-image reflection and resource hints

I faced an issue when running the application as a native image: the database URL appeared malformed. Spring’s [native samples repository](https://github.com/spring-attic/spring-native/tree/main/samples) had hints for specific technologies.

The error I encountered included `<unresolved>` in the database host:

```
Caused by: io.r2dbc.postgresql.PostgresqlConnectionFactory$PostgresConnectionException: Cannot connect to localhost/<unresolved>:5432
```

In my case, I added this hint for the R2DBC PostgreSQL driver:

```
@NativeHint(
		trigger = PostgresqlConnectionFactoryProvider.class,
		types = {
				@TypeHint(types = { Instant[].class, ZonedDateTime[].class, URI[].class }, access = {}),
		}
)
```


Reflection configuration can also be expressed in a `reflect-config.json` file. The exact mechanism depends on the GraalVM and Spring versions; use current Spring AOT and native-image documentation for new projects.

## Results

In this experiment, startup logs showed the following comparison:

Before:

```
Started MyApplicationKt in 13.374 seconds (JVM running for 16.857)
```

Now:

```
Started MyApplication in 0.129 seconds (JVM running for 0.132)
```

These are startup-time observations from one application, not a benchmark. I did not record comparable CPU and memory measurements, so the numbers alone do not show overall resource efficiency. For a current decision, measure cold and warm startup, memory, throughput, and latency under representative load.
