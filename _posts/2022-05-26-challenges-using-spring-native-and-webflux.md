---
title: Learnings from migrating a pet project to Spring Native and Webflux with PostgreSQL on Heroku
tags: Java Spring Native GraalVM 
style: fill
color: warning
description: I implemented a pet project using Spring Native and Webflux on Heroku, and those are my learning from it
layout: post
---

In my spare time last year, I created a pet project that aggregate news from some sources and delivers them to an Android app that I developed using Flutter, but that pet project is a topic for another post.

The backend for this pet project was firstly built using:

```
Kotlin
Gradle KTS
Spring Boot (Data, MVC, Security, Actuator)
PostgreSQL (Liquibase for migrations)
Deployed on a heroku free tier dyno (Validating the idea)
```

As I mentioned above, the stack is currently deployed in a Heroku free tier dyno, and that is a must for me to validate the idea for this project without spending tons of money. 

The MVP was deployed in heroku using one of their buildpacks for Gradle and everything was working fine with some struggles:

1 - When I was enriching the DB (POSTing more content), the response times increased a little bit.

2 - Since it is a pet project, the dyno running my app sleep sometimes during the day, and the initialization was very slow (Around 14 seconds)

Those problems were already bothering me, and I already saw a couple things about the reactive stack for Spring (Webflux / R2DBC) that could help me handle more requests on a peak load without scaling my infrasctructure.

Usually on my pet projects, I try to implement some new ideas (On this one, I improved my knowledge in Kotlin and learned Dart and Flutter), but I wasn't 100% sure that Webflux and Spring Native were mature enough for being used in this project (Even though is a pet project, there are currently 500+ MAU)

Skipping some time, I went to the We Are Developers Worldwide Conference in Berlin a couple weeks ago, where a lot of talks were showcasing the new Spring Native and the already "known" Spring Webflux.

So then, I gave that stack a try and those are my learnings from it:

## First mistakes

Those 2 technologies are somehow "new" and AFAIK, not being used in a lot of production grade environments.

Even the Spring project promises a lot of great improvements on Spring 6 and Spring Boot 3.0 for the GraalVM and Spring Native support.

With that being said, after some time, i realized that my first mistake was jumping into **BOTH** of the new technologies at the same time.

That created a feeling of not knowing if the issue was because of Webflux or Spring Native (I lost a couple nights of a lot of Stackoverflow and Github Issues trying to resolve the problems).

Then, I'll try to showcase the ones that I took notes and remember, please let me know if you faced other problems and we can spread the knowledge. 

### Heroku doesn't support Spring Native out of the box. Yet.

By it's nature of the AOT (Ahead of Time) compiler for the GraalVM, the Spring Native build consumes a lot of resources (It is a huge memory hog) and Heroku doesn't support it yet, so instead, you must build the image yourself or in your CI running `./gradlew bootBuildImage` , that will use a buildpack to build and generate a Docker image for you with your application.

Then, you just need to tag it with the `registry.heroku.com/<your_app_name>/<build>` , push and run `heroku container:release web -a <your_app_name>`.

Heroku has Docker containers support out of the box, so then it is the same as deploying using one of theirs buildpack.


### Spring Data Webflux and R2DBC drivers don't support a lot of nice features from relational databases

We know that Spring Webflux wasn't meant to be used with relational database since the JDBC drivers are I/O blocking, but the R2DBC initiative does it's job quite nicely.

Some features, such as the `@OneToMany` or `@ManyToMany` or `@ManyToOne` or `@OneToOne` are not supported (yet!) , and in order to make some things to work, you must add some annotations that are a little bit different, such as if you need auditing with the `@CreatedAt` and other annotations , you must add the `@EnableR2dbcAuditing` annotation.

Well, AFAIK, Quarkus and Micronaut already support some of those features with Native builds, so maybe this is something that Spring Data R2DBC will bring in the near future.

### Liquibase is NOT supported. Yet.

My first thought when implementing this project was to literally "copy/paste" most of the code from the project that is currently successfully running. 

And the database migration management tool that I was using is Liquibase (Wasn't a must, but instead, a good to have tool).

I started adding the Liquibase dependency and a lot of issues happened when building the native image, I resolved a lot of them but at the end, struggled with the fact that Liquibase currently doesn't support Spring Native with GraalVM out of the box, this is an issue for the future, hopefully when they chose their [issue](https://github.com/liquibase/liquibase/issues/1552) on Github, if you are interested, give a +1 on the thumbs up @ the issue!

### Most of the monitoring tools are not available. Yet.

One issue for production grade applications is observability and monitoring, so far, I couldn't find any way to make the Newrelic java agent to work together with the GraalVM and Spring Native builds (So, no APM yet!). But you can still instrument your application using the Metrics provided by the actuator and Micrometer with the interfaces to the best providers in the market (Datadog, Newrelic, Prometheus and others).

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
Started MyApplication in 0.129 seconds (JVM running for 0.132)
```

I'll try to update this post later with some insights on CPU and Memory consumption, but so far, nothing to complain!