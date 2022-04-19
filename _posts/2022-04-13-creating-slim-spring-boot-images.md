---
title: How to create slim Spring Boot docker images
tags: Java Technology Docker Spring Spring-Boot
style: fill
color: dark
description: How to create slim docker images for running your Spring Boot applications
layout: post
---

In this post, I will explain how you can create slim docker images by creating customized JREs using `jlink` and `jmods`.

Those commands are present on JDKs since Java 9, but actually being mature enough since Java 11, they bring a new way to create your customized JRE with only the modules that you need from Java, and then, creating smaller Docker images to run your Java applications (Mainly focused in Spring Boot applications), saving some good bucks in your Container Repository application (ECR, Artifactory, Docker Hub).

## But, how do we start?

Assuming you already have a JDK installed in your machine, if not, i strongly suggest you to use [sdkman.io](https://sdkman.io/) and install Java 17 version (Which is the latest LTS as of the date of this post)

First of all, we need to get the list produced from `jdeps` based in your jarfile from Spring Boot, for example:

```shell
$ jdeps --list-deps --ignore-missing-deps  your-fat-jar.jar
   java.base
   java.logging
```

Well, that doesn't seems right, huh?

Spring Boot has a strategy by default to generate a fat jar with all the needed dependencies inside of it, and `jdeps` currently can't get all the dependencies recursively inside the jars from the fat-jar.

So, what you can do is to extract all the contents from the fat-jar and run jdeps against every jar in the `lib` folder.

Or, you can try with try and error, and see which ClassNotFoundException you will get from each JRE version

But, from some previous experience, we usually need those packages in our minimal JRE:

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

But my suggestion is to try yourself and see which packages you will really need in your slim JRE

## Creating my Java slim JRE

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

You can get those informations as well by running `jlinks --help` in your command line tool.

## But then, how do I create my slim Spring Boot application docker image

Well, take this as an example, as i mentioned, it's using the OpenJDK 17 version (Latest LTS by the time this post was written)

```Dockerfile
# Build our minimal JRE using jlink

FROM openjdk:17 as builder

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

# Now it is time for us to build our real image on top of an slim debian image

FROM bitnami/minideb:bullseye

# Copy the JRE created in the last step into our $JAVA_HOME

COPY --from=builder /opt/jre-minimal $JAVA_HOME

# For gradle
# COPY build/libs/app.jar app.jar

# For maven
# COPY target/app.jar app.jar


ENTRYPOINT ["java","-jar","/app.jar"]
```

But, how efficient is this?

For example, in a regular spring boot application, it saved 200Mb of storage for every image generated, from `543.03` to `349.98`, assuming that you always have 10 versions of your application in your container registry, you can save **2** GB of storage space for each application!

