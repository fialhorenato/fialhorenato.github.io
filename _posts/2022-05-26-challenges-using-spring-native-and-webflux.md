---
title: Learnings from migrating a pet project to Spring Native and Webflux with PostgreSQL on Heroku
tags: Java Spring Native GraalVM 
style: fill
color: dark
description: I implemented a pet project using Spring Native and Webflux on Heroku, and those are my learning from it
layout: post
---

## Introduction

Hello!

It's been some time that i don't post here, but recently I created a pet project that aggregate news from some sources and delivers them to an Android app built using Flutter, but that is a topic for another post.

This pet project was firstly built using:

```
Kotlin
Spring Data
Liquibase
PostgreSQL
Spring MVC
Spring Security
OpenFeign
Heroku
```

And it was deployed in heroku using one of their buildpacks for Gradle, it was working fine, but sometimes it bothered me the startup time, since this is a pet project, i'm using the free dynos for now.

Everything was running smoothly, and then I went to the We Are Developers Worldwide Conference in Berlin last week, where everyone was talking about the new Spring Native and the already "known" Spring Webflux (The reactive stack of Spring), which I never even implemented a pet project with.

## First mistakes

Those 2 technologies are somehow "new" for a lot of Java/Kotlin developers, and a lot of drivers are still being implemented by the community, with a lot of features being missing.

After some time, i realized that my first mistake was jumping into **BOTH** of the new technologies at the same time, I faced some struggles from each project and struggles that both projects bring together, it was a little bit painful (2 nights of a lot of Stackoverflow and Github Issues) trying to resolve each problem.

## TIL

So, here are my TIL's from this project, and i hope to help anyone that will face the same problems as me.

### Heroku doesn't support Spring Native out of the box. Yet.

Unfortunately, the Spring Native build consumes a lot of resources and Heroku doesn't support it yet, so instead, you must build the image yourself or in your CI running `./gradlew bootBuildImage` , that will build and generate a Docker image for you with your application.

Then, you just need to tag it with the `registry.heroku.com/<your_app_name>/<build>` , push and run `heroku container:release web -a <your_app_name>`.

Hopefully this will change in the future.


### Spring Data Webflux and R2DBC drivers don't support a lot of nice features from relational databases

We know that Spring Webflux wasn't meant to be used with relational database since the nature of the JDBC is I/O blocking, but the R2DBC does it's job quite nicely.

Some features, such as the `@OneToMany` or `@ManyToMany` or `@ManyToOne` or `@OneToOne` are not supported, and in order to make some things to work, you must add some annotations that are a little bit different, such as if you need auditing with the `@CreatedAt` and other annotations , you must add the `@EnableR2dbcAuditing` annotation.

Well, AFAIK, Quarkus and Micronaut already support some of those features with Native images, so maybe this is something that Spring Data will bring in the near future.

### Liquibase is NOT supported. Yet.

My first thought when implementing this project was to literally "copy/paste" most of the code from the project that is currently successfully running. And the database migration management tool that I was using is Liquibase.

I started adding the Liquibase dependency and a lot of issues happened when building the native image, I resolved a lot of them but at the end, struggled with the fact that Liquibase currently doesn't support Spring Native with GraalVM out of the box, this is an issue for the future, hopefully when they chose their [issue](https://github.com/liquibase/liquibase/issues/1552) on Github, if you are interested, give a +1 on the thumbs up @ the issue!

### You must provide some hints to the GraalVM, and some of them are not 100% clear

I faced an issue when running my application as a native app because the database URL was becoming malformed somehow, then, after a lot of research I found the [samples repo]() from Spring that had a lot of tips to use Spring Native with some specific technologies.

The error that i was facing was an `<unresolved>` showing up from nowhere in the middle of my database URL:

```
Caused by: io.r2dbc.postgresql.PostgresqlConnectionFactory$PostgresConnectionException: Cannot connect to localhost/<unresolved>:5432
```

In my case, in order to use the R2DBC PostgreSQL and Spring Native, i had to add this hint to the GraalVM:

```
@NativeHint(
		trigger = PostgresqlConnectionFactoryProvider.class,
		types = {
				@TypeHint(types = { Instant[].class, ZonedDateTime[].class, URI[].class }, access = {}),
		}
)
```


You can have a `META-INF/native/reflect-config.json` file as well.

## Results

Well, now, let's come to the results measured so far:

Before:

```
Started MyApplicationKt in 13.374 seconds (JVM running for 16.857)
```

Now:

```
Started MyApplication in 0.788 seconds (JVM running for 1.17)
```

I'll try to update this post later with some insights on memory consumption and requests, but so far, nothing to complain.