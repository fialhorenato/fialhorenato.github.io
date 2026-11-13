---
title: "Graceful Shutdown for Spring Boot in Docker and Kubernetes"
tags:
  - Java
  - Spring Boot
  - Docker
  - Kubernetes
description: Configure graceful Spring Boot shutdowns so active requests can finish during container restarts in Kubernetes or ECS.
last_modified_at: 2026-11-13
layout: single
---

When an orchestrator stops a container, the application usually receives SIGTERM and has a limited time to finish active work before it is forcefully terminated with SIGKILL. This article shows how to enable graceful shutdown for a Spring Boot web application and why the orchestrator’s termination grace period must allow the application enough time to stop.

## Why graceful shutdown matters

I'll try to make this as simple as possible, and for that, i'll try to bring an illustration on how a "regular" architecture of a Spring Boot Service looks like inside an orchestrator:

![alt text](/images/springbootapp.png "Your amazing spring boot app")

The issue happens when the load balancer needs to drain the connections towards that task, but we still need to handle the `keep-alive` connections, just as saw in this image from AWS ELB on ECS instances:

![alt text](/images/awselb.png "ELB Connection Drain")

And weirdly (or not), the Spring Boot web containers are by default, expected to shutdown `IMMEDIATELY` instead of `GRACEFULLY` , and that can cause some keep-alive connections to fail on the ingress car, and consequently, returns 5xx errors in the load balancer.

## Enable graceful shutdown

For Spring Boot versions that support graceful shutdown, enable it in `application.properties` or `application.yml`:

```
    server.shutdown=graceful
```

OR

```yml
server:
    shutdown: graceful
```

This shutdown allows the web server to support graceful shutdown, allowing active requests time to complete and closing the `keep-alive` connections towards your service.

Set the phase timeout to match the longest request you intend to let finish, and configure the container platform’s termination grace period to allow at least that long plus time for the process to stop. The exact behavior depends on the server and Spring Boot version; see the [Spring Boot graceful shutdown reference](https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html).
