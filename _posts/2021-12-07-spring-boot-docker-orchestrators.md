---
title: Handling SIGTERM and SIGKILL in Spring Boot Applications running on Docker Orchestrators (Kubernetes, ECS)
tags: Java Technology Docker
style: fill
color: light
description: How to handle SIGTERM and SIGKILL instructions in Spring Boot Web Applicatons running on Docker Orchestrators
layout: post
---

In this post, i'll mainly focus on some learnings we've been having with Spring Boot Web Applications running embedded web containers (Tomcat, Undertow, Jetty...) and how to properly handle SIGTERM and SIGKILL instructions, since those are super relevant when working in an Docker Orchestrator environments with Kubernetes, ECS, GCE or something like that.

## But what is the use case?

I'll try to make this as simple as possible, and for that, i'll try to bring an illustration on how a "regular" architecture of a Spring Boot Service looks like inside an orchestrator:

![alt text](/images/springbootapp.png "Your amazing spring boot app")

The issue happens when the load balancer needs to drain the connections towards that task, but we still need to handle the `keep-alive` connections, just as saw in this image from AWS ELB on ECS instances:

![alt text](/images/awselb.png "ELB Connection Drain")

And weirdly (or not), the Spring Boot web containers are by default, expected to shutdown `IMMEDIATELY` instead of `GRACEFULLY` , and that can cause some keep-alive connections to fail on the ingress car, and consequently, returns 5xx errors in the load balancer.

## And how do I fix this?

So, in order to fix that, you must add a line to your `application.properties` or `application.yml` file like this:

```
    server.shutdown=graceful
```

OR

```yml
server:
    shutdown: graceful
```

This shutdown allows the web server to support graceful shutdown, allowing active requests time to complete and closing the `keep-alive` connections towards your service.