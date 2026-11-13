---
title: "Migrating from Spring Boot 2.7 to 3.0: Kotlin Notes"
tags:
  - Software Development
description: Notes from migrating a Kotlin application from Spring Boot 2.7 to 3.0, including Spring Security and Jakarta package changes.
last_modified_at: 2026-11-13
layout: single
---

This is a historical account of migrating my [SpringBootstrap](https://github.com/fialhorenato/SpringBootstrap) project from Spring Boot 2.7 to 3.0 in 2022. The examples reflect that release; for a current upgrade, use the migration guide for your target Spring Boot version.

You can see the PR with the changes [here](https://github.com/fialhorenato/SpringBootstrap/pull/215)


## Disclaimer

There is an [official Spring Boot 3.0 migration guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide). Check the Spring documentation for the migration guide matching the version you plan to use.

Even though Spring 3.0.0 is GA, the version 2.7.x will receive OSS Support until the end of 2023, and commercial support until begin 2025.

For production systems, plan and test framework upgrades against your application’s dependencies and operational requirements.


## What changed in Spring Boot 3.0?

Yes! And it is bringing Spring 6 support to Spring Boot, which will bring some breaking changes but a lot of great support to new features of the language and to the future of Jakarta EE (Former JavaEE).

As well, it will bring more support to the GraalVM and Native applications, making the Spring Boot applications more competitive on containers and cloud environments.

## Migrating

The application I migrated to Spring Boot 3.0 was a small project that I use as a starting point for other work. It had a limited dependency set and an established test suite.

Another thing to mention is that my application was already designed for **Java 17**, which is the minimum to run the Spring Boot 3.0.0, if you didn´t had time to migrate your applications to Java 17, please do it, it worth.

My main pain points bringing it up to date were the new Spring Security way of implementing `SecurityFilterChain` and the changes from `javax.persistence.*` to `jakarta.persistence.*` and `javax.servlet.*` to `jakarta.servlet.*`.


## WebSecurityConfigurerAdapter is gone

Well, as the name of the section states, the `WebSecurityConfigurerAdapter` is gone, and Spring now relies in a `SecurityFilterChain` bean to configure your http requests security configuration.

### How it was

This is how it is using the `WebSecurityConfigurerAdapter` on Spring 2.7.x.
```java
    @EnableWebSecurity
    @EnableGlobalMethodSecurity(securedEnabled = true)
    class SecurityConfig(private val jwtAuthorizationFilter: JwtAuthorizationFilter) : WebSecurityConfigurerAdapter() {

        override fun configure(http: HttpSecurity) {
            http
                .cors().and()
                .csrf().disable()
                .sessionManagement().sessionCreationPolicy(STATELESS).and()
                .authorizeRequests()
                .antMatchers("/security/**").permitAll()
                .requestMatchers(toAnyEndpoint()).permitAll()
                .antMatchers("/hello-world/insecure").permitAll()
                .antMatchers("/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
                .anyRequest().authenticated()
                .and()
                .addFilterBefore(jwtAuthorizationFilter, UsernamePasswordAuthenticationFilter::class.java)
        }
    }
```

### How it is now

Since `WebSecurityConfigurerAdapter` was removed, the security configuration moves to a `SecurityFilterChain` bean. The class is annotated with `@Configuration` so Spring can register the bean.

The `@EnableGlobalMethodSecurity` is being deprecated as well in favor of `@EnableMethodSecurity`

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(
        securedEnabled = true
)
class SecurityConfig(private val jwtAuthorizationFilter: JwtAuthorizationFilter) {

    @Bean
    fun configure(http: HttpSecurity): SecurityFilterChain {
        http
                .cors().and()
                .csrf().disable()
                .sessionManagement().sessionCreationPolicy(STATELESS).and()
                .authorizeHttpRequests {
                    it.requestMatchers("/security/**").permitAll()
                            .requestMatchers(toAnyEndpoint()).permitAll()
                            .requestMatchers("/hello-world/insecure").permitAll()
                            .requestMatchers("/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
                            .anyRequest()
                            .authenticated()
                            .and()
                            .addFilterBefore(jwtAuthorizationFilter, UsernamePasswordAuthenticationFilter::class.java)
                }

        return http.build();
    }
```


## Javax is gone, welcome Jakarta

The JavaEE project was taken over by the Eclipse foundation and became [JakartaEE](https://jakarta.ee/), which will be the future standard for building enterprise applications using Java.

With that said, the `javax.*` package naming must be substituted by `jakarta.*`.

Some changes were made in the persistence part of Jakarta, but usually this change shouldn´t break anything in your project.

One easy way of doing this is by replacing every `javax` entry in your code to `jakarta`, but be in mind that problems can happen and you must be able to troubleshoot.


## Conclusions

With that being said, the migration from 2.7.x to 3.0.0 was easier than I expected, but I'm super excited for the future of the Spring Boot versions and the new support to JakartaEE
