---
title: How to create slim Spring Boot docker images
tags: Java Technology Docker Spring Spring-Boot
style: fill
color: warning
description: How to create slim docker images for running your Spring Boot applications
layout: post
---

Today, we are going to talk about the JRE, and how we can create slim docker images by creating customized JREs using `jlink` and `jmods`.

Since `Java 9` , but more mature since `Java 11`, the JDK contains a new way to create your customized JRE with only the modules that you need from Java, and with that, you can save some good bucks in your Container Repository application (ECR, Artifactory, Docker Hub).

But, how do we start?

First, we need to get the list produced from `jdeps` based in your jarfile from Spring Boot, for example:

```shell
$ jdeps --list-deps --ignore-missing-deps  your-fat-jar.jar
   java.base
   java.logging
```
Spring boot already generates a fat jar with all the needed dependencies inside of it, so not many dependencies from java are needed in the JRE, if you want to check all the dependencies, you can just remove the `--ignore-missing-deps` and check inside your JAR if your dependencies are already met.

So, for example, we can create our docker image like this:

```Dockerfile
FROM openjdk:17 as builder

USER root

RUN apk --update add --no-cache --virtual .jlink-build-deps binutils=~2.34-r2 && \
    jlink \
    --module-path "$JAVA_HOME/jmods" \
    --add-modules java.base, java.logging \
    --verbose \
    --strip-debug \
    --compress 2 \
    --no-header-files \
    --no-man-pages \
    --output /opt/jre-minimal

USER app

# img
FROM openjdk:17-alpine

WORKDIR /app

COPY --from=builder /opt/jre-minimal $JAVA_HOME
COPY --from=builder /opt/java/lib/security/cacerts "$JAVA_HOME"/lib/security/cacerts

# For gradle
# COPY build/libs/app-*.jar build/app.jar

# For maven
# COPY target/app-*.jar build/app.jar

WORKDIR /app/build
ENTRYPOINT java -jar app.jar
```

But, how efficient is this?

For example, in a regular spring boot application, it saved 200Mb of storage for every image generated, from `543.03 MB` to `349.98 MB`, assuming that you always have 10 versions of your application in your container registry, you can save `2GB` of storage space for each application!

