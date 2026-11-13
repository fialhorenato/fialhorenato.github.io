---
date: 2026-11-06
title: "Spring Boot Kubernetes Probes: Liveness, Readiness, Startup"
description: "Configure Spring Boot Actuator health probes for Kubernetes and understand when to use liveness, readiness, and startup checks without causing restart loops."
tags:
  - Software Development
layout: single
---

Kubernetes health probes look like a small YAML detail, but the wrong check can turn a slow dependency into a restart loop—or send traffic to a Spring Boot instance that has not finished starting.

This guide explains the difference between liveness, readiness, and startup probes, then shows a practical Spring Boot Actuator configuration. It focuses on the decisions that matter in production: which port the probe reaches, what happens when a dependency fails, and how probe settings interact with graceful shutdown.

If you are already configuring shutdown behavior, see my related guide to [graceful shutdown for Spring Boot in Docker and Kubernetes](/blog/spring-boot-docker-orchestrators).

## The three Kubernetes probes answer different questions

Kubernetes reacts differently to each probe result, so they should represent different conditions:

| Probe | Question | Failure action |
| --- | --- | --- |
| **Liveness** | Is the process so unhealthy that restarting it may help? | Kubernetes restarts the container after the configured failures. |
| **Readiness** | Should this instance receive traffic right now? | Kubernetes keeps it running but removes it from ready service endpoints. |
| **Startup** | Has this application finished starting? | Kubernetes waits before running liveness and readiness checks. |

A startup probe is useful when startup can take longer than the normal liveness window. Once it succeeds, Kubernetes starts the liveness and readiness probes. The [Kubernetes probe documentation](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/) describes the timing and failure behavior.

## Enable Spring Boot Actuator probes

Add Spring Boot Actuator to the application, then configure the health probe paths. In Spring Boot versions that support additional probe paths on the main server port, this configuration exposes `/livez` and `/readyz`:

```yaml
management:
  endpoint:
    health:
      probes:
        add-additional-paths: true
```

Spring Boot provides the liveness and readiness health groups for Kubernetes deployments. Additional paths on the main application port are helpful when management endpoints use a separate port: a successful check on a different web server does not prove that the application’s request-handling port is accepting connections. See the [Spring Boot Actuator health endpoint reference](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html) and verify the property against the exact Spring Boot version you run.

Only expose the Actuator endpoints the platform needs. Spring Boot exposes only a limited set by default; endpoints can reveal operational details, so do not expose the full Actuator surface publicly just to support health checks.

## Configure the probes in your Pod

Here is a starting point for a Kubernetes container using the main application port and Spring Boot’s additional health paths:

```yaml
containers:
  - name: application
    ports:
      - name: http
        containerPort: 8080
    startupProbe:
      httpGet:
        path: /livez
        port: http
      periodSeconds: 10
      failureThreshold: 30
    livenessProbe:
      httpGet:
        path: /livez
        port: http
      periodSeconds: 10
      timeoutSeconds: 2
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /readyz
        port: http
      periodSeconds: 5
      timeoutSeconds: 2
      failureThreshold: 3
```

These values are examples, not universal production defaults. Set the startup window from observed startup times, and keep the HTTP timeout above the normal response time of the health endpoint. If the application uses the default Actuator paths instead, point probes at `/actuator/health/liveness` and `/actuator/health/readiness`.

The startup probe’s maximum initial allowance is roughly `periodSeconds × failureThreshold` (30 × 10 seconds in this example). Once it succeeds, liveness checks take over. This avoids weakening the liveness policy just because an application needs more time during startup.

## Keep liveness independent of external systems

Do not make liveness fail because a database, cache, or downstream API is temporarily unavailable. A liveness failure tells Kubernetes to restart the application. If every replica fails liveness because they all depend on one unavailable service, Kubernetes can restart the entire fleet without repairing the dependency and add more load during an outage.

Liveness should indicate an internal condition where restarting the process is a reasonable recovery action—for example, a detected deadlock or an application state that cannot recover in place. If the process exits when it cannot continue, Kubernetes already restarts it according to the Pod’s restart policy; a custom liveness check is not always necessary.

## Use readiness for traffic decisions

Readiness should answer whether this instance can serve requests now. Spring Boot’s default readiness group does not include every external health indicator. That is deliberate: an unavailable optional dependency should not necessarily remove every application instance from service.

Add a dependency check only when the application cannot safely serve requests without that dependency and removing this instance from traffic is the correct operational response. Consider whether partial functionality, retries, fallback behavior, or a degraded response is preferable. Readiness checks should be fast and bounded; they run repeatedly and can themselves add load to a struggling dependency.

An instance can be unready while remaining live. That is useful during startup, maintenance, or a graceful shutdown when the process still needs to finish in-flight work but should receive no new traffic.

## Check probe paths, security, and shutdown together

Before deploying, verify that:

- The configured path returns a success status when the instance is healthy.
- Kubernetes can reach the port where the health endpoint is served.
- Security filters allow the kubelet’s probe request without opening sensitive Actuator endpoints to the public.
- The liveness group does not depend on databases or remote APIs.
- Readiness reflects whether the instance should receive traffic, not whether every optional service is perfect.
- The startup window covers real worst-case initialization time.
- The termination grace period allows readiness to change and in-flight requests to finish during shutdown.

Spring Boot’s [graceful shutdown support](https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html) can stop accepting new requests while active requests complete. The orchestrator’s termination grace period must leave enough time for that process to finish before forceful termination.

## A practical rule of thumb

Use **liveness** to decide whether restarting may recover the process, **readiness** to decide whether it should receive traffic, and **startup** to protect slow initialization from premature restarts. Keep each signal narrow, test it during dependency failures and shutdown, and tune its timing from observed behavior.

For the exact properties and health group behavior, consult the [Spring Boot Actuator reference](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html) and the [Kubernetes probe guide](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).
