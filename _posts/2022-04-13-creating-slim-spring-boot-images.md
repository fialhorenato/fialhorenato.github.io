---
title: "Build Smaller Spring Boot Docker Images with jlink"
tags:
  - Software Development
description: "Use jdeps and jlink to create a custom Java runtime for a Spring Boot Docker image, with a historical Java 17 example and compatibility caveats."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
translation_url: "/blog/imagens-spring-boot-docker-menores-jlink"
translation_label: "Leia este artigo em português"
---

This 2022 walkthrough shows how I used `jdeps` and `jlink` to build a smaller Java runtime for a Spring Boot Docker image. It uses Java 17-era image names and commands; review the base images, Java version, and module list for your current application before adopting it.

`jdeps` and `jlink` have been available since Java 9. They can help create a custom runtime containing selected JDK modules, which may reduce the size of a Java application image. The result depends on the application, dependencies, base image, and build process; measure the final image and test the runtime carefully.

## Inspect the application dependencies

Use a JDK version supported by your application and build the runtime with the same JDK release. The commands below reflect a Java 17 setup from 2022.

Start by inspecting the application with `jdeps`:

```shell
$ jdeps --list-deps --ignore-missing-deps  your-fat-jar.jar
   java.base
   java.logging
```

If the output looks incomplete, that is expected for a Spring Boot executable archive:

Spring Boot packages application dependencies inside a nested `BOOT-INF/lib` directory. A basic `jdeps` run on the outer archive may not analyze every nested dependency recursively.

Extract the archive and analyze the application classes and dependency JARs individually, or use a build-time dependency-analysis workflow. Then verify the module list by running the application with the linked runtime and exercising code paths that may load classes reflectively. A `ClassNotFoundException` at runtime is a late signal, so include integration tests.

In my previous projects, the following modules were common starting points—not a guaranteed list for every Spring Boot application:

```
java.compiler
java.logging
java.sql
java.rmi
java.naming
java.management
java.instrument
java.security.jgss
java.net.http
jdk.httpserver
jdk.naming.dns
```

Treat this list as a starting point from one application, not a reusable module set. Determine the required modules for your own app and libraries, and rerun analysis when dependencies change.

## Build a custom Java runtime with jlink

You can use `jlink` locally to create your customized JRE, the command is somehow like this:

```shell
jlink \
    --module-path "$JAVA_HOME/jmods" \
    --add-modules [the java modules your application needs joined by ,]] \
    --verbose \
    --strip-debug \
    --compress 2 \
    --no-header-files \
    --no-man-pages \
    --output /opt/jre-minimal
```

Explaining each flag:

```
--module-path <path>              Module path.
                                        If not specified, the JDKs jmods directory
                                        will be used, if it exists. If specified,
                                        but it does not contain the java.base module,
                                        the JDKs jmods directory will be added,
                                        if it exists.

--verbose                         Enable verbose tracing

--strip-debug                     Strip debug information

--compress=<0|1|2>                Enable compression of resources:
                                          Level 0: No compression
                                          Level 1: Constant string sharing
                                          Level 2: ZIP

--no-header-files                 Exclude include header files

--no-man-pages                    Exclude man pages

--output <path>                   Location of output path
```

For the options supported by your installed JDK, run `jlink --help`.

## Package the runtime with a Spring Boot application

This illustrative multi-stage Dockerfile uses Java 17-era image names and should be updated for a supported base image and the target JDK before use.

```Dockerfile
# Build a minimal runtime with jlink

FROM openjdk:17 AS builder

USER root

RUN jlink \
    --module-path "$JAVA_HOME/jmods" \
    --add-modules java.compiler,java.sql,java.naming,java.management,java.instrument,java.rmi,java.desktop,jdk.internal.vm.compiler.management,java.xml.crypto,java.scripting,java.security.jgss,jdk.httpserver,java.net.http,jdk.naming.dns,jdk.crypto.cryptoki,jdk.unsupported \
    --verbose \
    --strip-debug \
    --compress 2 \
    --no-header-files \
    --no-man-pages \
    --output /opt/jre-minimal

USER app

# Assemble the application image on a compatible base

FROM bitnami/minideb:bullseye

# Add the custom runtime

COPY --from=builder /opt/jre-minimal $JAVA_HOME

# Copy the application JAR built by Gradle
# COPY build/libs/app.jar app.jar

# Or copy the application JAR built by Maven
# COPY target/app.jar app.jar


ENTRYPOINT ["java","-jar","/app.jar"]
```

## Measure the image-size result

In my 2022 example, the resulting image was about 200 MB smaller than the original. Your result will vary with the application and base image, and registries may deduplicate shared layers, so measure actual stored and transferred size rather than assuming the same saving.

