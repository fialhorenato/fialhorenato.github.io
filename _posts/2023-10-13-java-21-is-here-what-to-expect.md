---
title: Java 21 is here, what to expect on Spring Boot
tags: Java Development Spring
style: fill
color: warning
description: Best features for Java 21 on Spring Boot
layout: post
---

In this post, I'll focus on the new features that Java 21 will bring to Spring Boot and how to take advantage of them.

### Disclaimer

As of the moment that I'm writing this post, Java 21 is released but not adopted on Kotlin version 1.9.10, we expect maybe that the version 1.9.20 brings compatibility to it, then, so far no Kotlin.

## Features

### Level pattern matching with records, switch and if

The enhanced switch pattern matching is amazing, and it will help a lot on writing simple, readable and concise code.

```java
if (o instanceof Event(Instant instant)) {
    System.out.println("This event happened in " + instant.toEpochMilli());
}

return switch (o) {
    case UserDeletedEvent(var user) -> "the user " + user.name() + " has been deleted";
    case UserCreatedEvent(var name) -> "the new user with name " + name + " has been created";
    default -> null;
};
```


### Virtual Threads and Project Loom

You probably hear a lot about Loom. The project that will make any code fast and scalable by using virtual threads!

After project Loom we won't be capped by the number of threads on the OS, we will be able to create cheaper threads for the heap!

As of now, Spring Boot and Tomcat doesn't support virtual threads very easily out of the box, but it is expected to have on version 3.2.0 that it will be as easy as a property to be set.

```yaml
spring:
    threads:
        virtual:
            enabled: true
```
 

Or simply `spring.threads.virtual.enabled=true` on your `.properties` file.


## Conclusion

Java 21 comes to change the way we write code in Java, and to bring the scalability that modern langagues in an easy way, such as reactive programming, etc.




