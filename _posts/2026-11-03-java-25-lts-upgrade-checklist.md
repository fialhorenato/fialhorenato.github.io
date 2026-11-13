---
date: 2026-11-03
title: "Java 25 LTS Upgrade Checklist for Spring and Java Applications"
description: "Plan a Java 25 LTS migration with this checklist for dependency compatibility, CI and containers, runtime testing, observability, and safe rollout."
tags:
  - Java
  - Java 25
  - Migration
  - Spring Boot
layout: single
---

Java 25 is an LTS release in Oracle’s support roadmap, and it arrived in September 2025. For teams running Java 17 or 21, that makes it a useful point to assess the next runtime upgrade. An LTS label does not guarantee that every vendor has the same support policy, so confirm the lifecycle and licensing terms for the JDK distribution you deploy.

This checklist focuses on the migration work that tends to matter more than syntax: dependency compatibility, build and runtime images, tests, observability, and a controlled rollout. It is not a claim that every Java 21 application can be moved to Java 25 without changes.

I previously wrote about [Java 19 virtual threads while they were still a preview feature](/blog/working-with-new-virtual-threads-java-19). This guide takes a broader upgrade perspective and treats preview APIs separately from production migration work.

## 1. Start with your runtime and support policy

Record the JDK distribution, exact version, patch cadence, and support terms used in each environment. Development, CI, containers, serverless runtimes, and production hosts should not silently drift apart.

Choose a supported Java 25 distribution and set a patch-update process. LTS designation and commercial support are vendor-specific; Oracle’s [Java SE support roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html) identifies Java 25 as an LTS release in Oracle’s product schedule.

Before changing the runtime, capture a baseline for startup time, memory use, garbage collection, throughput, latency, and error rates. Those measurements give you a concrete comparison after the upgrade.

## 2. Inventory frameworks, libraries, and build tools

Check the support matrix for your application framework, build plugins, bytecode tools, agents, serializers, database drivers, and test libraries. Pay particular attention to components that inspect or transform bytecode, use reflection, generate proxies, or depend on internal JDK APIs.

Update the build tool and plugins to versions that support the chosen JDK. Run dependency convergence and vulnerability checks after the upgrade; a runtime change can expose transitive dependency combinations that were not previously resolved or exercised.

For Spring applications, verify the supported JDK range for the exact Spring Boot release you use. Upgrade the framework and the Java runtime as separate changes where practical, so a failure has a smaller search space.

## 3. Update the JDK in every build and deployment layer

Changing `JAVA_HOME` on a developer laptop is not enough. Update the JDK used by:

- Local development and IDE project settings.
- Maven or Gradle toolchains and compiler configuration.
- Continuous integration runners and test containers.
- Docker build and runtime images.
- Kubernetes base images, serverless runtimes, and deployment manifests.
- Static analysis, coverage, and observability agents.

Pin an explicit image tag or digest for repeatable builds. Avoid relying on a floating `latest` tag, and confirm that the selected image is maintained and appropriate for your security requirements.

Keep the bytecode target explicit during a staged migration. You can run tests on Java 25 while still producing bytecode for an older baseline, if your deployment strategy requires it. Remove that compatibility setting only when all supported consumers are ready.

## 4. Test behavior on the new runtime

Run unit, integration, contract, and end-to-end tests on Java 25. Include tests for serialization, TLS, database access, scheduled jobs, asynchronous work, and shutdown behavior—especially if those areas rely on JDK or framework internals.

Use the [Java migration guide](https://docs.oracle.com/en/java/javase/25/migrate/) and release notes to review changes relevant to your application. Search startup logs for illegal reflective access, removed options, agent warnings, and deprecated APIs. Treat warnings as migration tasks with an owner rather than suppressing them globally.

Then run representative load tests and compare them with the baseline. A successful compile proves that the code builds; it does not show that latency, memory use, or operational behavior stayed acceptable.

## 5. Review JVM flags and observability

Do not carry forward every historical JVM option by habit. Check each flag against Java 25 documentation, remove obsolete settings, and change only what measurements justify. Recheck container memory limits, heap sizing, garbage-collection logs, and crash diagnostics in the actual runtime image.

Verify that monitoring agents and profilers support the new JDK. Confirm that your dashboards still capture the metrics you use to detect regressions, and make sure deployment rollback restores the previous runtime and image as a unit.

## 6. Adopt Java 25 features separately from the runtime upgrade

Java 25 includes several language and library changes, but adopting them is optional. For example, [JEP 512](https://openjdk.org/jeps/512) finalizes compact source files and instance `main` methods, and [JEP 511](https://openjdk.org/jeps/511) adds module import declarations. These features can simplify small programs and examples; they do not require rewriting mature application code.

Some concurrency features remain preview features. In particular, [JEP 505](https://openjdk.org/jeps/505) is the fifth preview of structured concurrency in Java 25. Preview APIs require explicit enablement and can change between releases, so evaluate them separately from a production runtime migration.

Keep the first upgrade focused on running your existing application reliably. Adopt new language features later, in small changes with their own review and tests.

## 7. Roll out with a measurable rollback plan

Deploy to a representative staging environment first, then release to a small production slice if your platform supports it. Compare health checks, startup, latency percentiles, memory, CPU, garbage collection, and downstream error rates against the baseline.

Write down the rollback trigger before the rollout. Make sure the previous JDK image remains available and that state changes made by the application remain compatible with the old version. A runtime rollback is not safe if the new release also made an irreversible schema or data-format change.

## Java 25 upgrade checklist

- Confirm the JDK vendor’s support policy and patch process.
- Verify Spring Boot, build plugins, agents, and dependencies support Java 25.
- Update local, CI, test, and deployment JDKs consistently.
- Run the complete test suite and review runtime warnings.
- Benchmark representative workloads against a recorded baseline.
- Revisit JVM flags, memory limits, and observability agents.
- Separate preview features and source modernization from the runtime upgrade.
- Roll out gradually with measurable rollback criteria.

The safest Java 25 migration is a controlled runtime change: establish a baseline, verify the dependency ecosystem, test real workloads, and roll out with a clear rollback path. New Java features can follow once the application is stable on the new JDK.
