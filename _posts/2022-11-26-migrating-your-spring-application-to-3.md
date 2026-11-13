---
title: "Migrating a Kotlin Application from Spring Boot 2.7 to 3.0"
tags:
  - Software Development
description: "A historical migration report covering Spring Security configuration and the javax-to-Jakarta package change in Spring Boot 3.0."
last_modified_at: 2026-11-13
layout: single
---

This article documents my 2022 migration of [SpringBootstrap](https://github.com/fialhorenato/SpringBootstrap) from Spring Boot 2.7 to 3.0. See the changes in [pull request 215](https://github.com/fialhorenato/SpringBootstrap/pull/215).

> **Historical guide:** The examples target Spring Boot 3.0. For a current upgrade, use the migration guide for your target Spring Boot release.

## Before migrating

Spring Boot 2.7 and 3.0 support timelines have moved on. Check the lifecycle information for the distribution you use. For production systems, plan and test framework upgrades against your dependencies and operational requirements.

## What changed in Spring Boot 3.0?

Spring Boot 3.0 is based on Spring Framework 6 and requires Java 17. The upgrade also introduced breaking changes, including the move from Java EE `javax.*` APIs to Jakarta EE `jakarta.*` APIs. Spring Boot 3.0 also added support for native-image workloads, though build configuration and library compatibility require separate evaluation.

The application was a small starter project with a limited dependency set and an established test suite. It already targeted Java 17, the minimum for Spring Boot 3.0. If your application uses an older JDK, include the Java upgrade in the plan and validate it in the deployment environment.

The main changes I encountered were the Spring Security `SecurityFilterChain` configuration and the move from affected `javax.persistence.*` and `javax.servlet.*` APIs to their `jakarta.*` equivalents.

## Replace `WebSecurityConfigurerAdapter` with `SecurityFilterChain`

Spring Security no longer uses `WebSecurityConfigurerAdapter` in this configuration style. Define a `SecurityFilterChain` bean to configure HTTP request authorization and related security behavior.

### Before: Spring Boot 2.7

This is the configuration pattern used by my Spring Security 5.7-era application before the migration:
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

### After: Spring Boot 3.0

After removing `WebSecurityConfigurerAdapter`, I moved the rules into a `SecurityFilterChain` bean registered by a `@Configuration` class.

For this migration, I also replaced `@EnableGlobalMethodSecurity` with `@EnableMethodSecurity`. Check the API appropriate to your Spring Security version.

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

## Migrate Java EE imports to Jakarta EE

Jakarta EE is the continuation of Java EE under the Eclipse Foundation. Spring Boot 3 uses Jakarta EE APIs for the areas covered by this migration.

For affected APIs, imports move from `javax.*` to `jakarta.*`. Do not blindly replace every `javax` package: Java SE packages such as `javax.sql` remain under `javax`, so review compiler errors and dependency documentation.

The namespace change can affect application code, dependencies, configuration, and generated sources, so compile and run integration tests after updating dependencies.

## Takeaway

For this project, the migration was easier than I expected. The main work was concentrated in the security configuration and namespace changes. Your effort will depend on dependency compatibility, test coverage, and application-specific use of the affected APIs.
