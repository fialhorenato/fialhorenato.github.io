---
title: "Reduce Java Boilerplate with Project Lombok"
tags:
  - Java
  - Project Lombok
  - Developer tools
description: See how Project Lombok generates Java getters, setters, constructors, equals, hashCode, and logging code from annotations.
last_modified_at: 2026-11-13
layout: single
---

Have you spent time writing—or generating in an IDE—the same Java getters, setters, constructors, and utility methods? A simple data class can require getters, setters, constructors, toString, equals, and hashCode.

Languages such as Kotlin and Scala reduce some of this boilerplate. Java developers can also use Project Lombok, which generates common methods from annotations.

# Project Lombok
That's how project Lombok describes themselves:

> Project Lombok is a java library that automatically plugs into your editor and build tools, spicing up your java.
> Never write another getter or equals method again, with one annotation your class has a fully featured builder, Automate your logging variables, and much more.

Lombok uses annotations and generates code during compilation. This can keep source files shorter, though teams should weigh that convenience against the extra IDE and build configuration.

![alt text](/images/annotations-everywhere.jpg "Annotations Everywhere")

In order to use Lombok, you need to install the plugin for your specific IDE.

- Check [here](https://projectlombok.org/setup/eclipse) for the instructions for eclipse
- Check [here](https://plugins.jetbrains.com/plugin/6317-lombok) for the plugin for IntelliJ
- Check [here](https://projectlombok.org/setup/netbeans) for Netbeans (Please make a favor to yourself and migrate to [IntelliJ Community](https://www.jetbrains.com/idea/download))

## Getters, Setters, toString, equals and hashCode

Then this:

```java
public class Person{
  private String name;
  private int age;

  public String getName(){
    return name;
  }
  
  public void setName(String name){
    this.name = name;
  }
  
  public int getAge(){
    return age;
  }
  
  public void setAge(int age){
    this.age = age;
  }
  
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    Person person = (Person) o;
    return name == person.name &&
        age == person.age;
  }

  @Override
  public int hashCode() {
    return Objects.hash(name, age);
  }

  @Override
  public String toString() {
    return "Person{" +
        "name=" + name +
        ", age=" + age +
        '}';
  }
}
```

Will be reduced to only:

```java
@Data
public class Person{
  private String name;
  private int age;
}
```

![alt text](/images/magic.gif "Magic")

[@Data](https://projectlombok.org/features/Data) provides you @ToString, @EqualsAndHashCode, @Getter on all fields, @Setter on all non-final fields, and @RequiredArgsConstructor.

## Logging never was so easy!

Lombok helps you to log easily with the logging library that you choose for your project. It has support to Log4j, Log4j2, Sl4j, CommonsLog and others.

Check the [@Log](https://projectlombok.org/features/log) page.

## Immutable classes

The [@Value](https://projectlombok.org/features/Value) annotation can make immutable classes more concise:

> `@Value` is the immutable variant of `@Data`: fields are private and final by default, setters are not generated, and Lombok generates methods such as `toString()`, `equals()`, `hashCode()`, getters, and an all-arguments constructor. See the [official `@Value` documentation](https://projectlombok.org/features/Value) for details.

I'll write a post in the future of the pros and cons for Immutable classes in Java, but it's a great POJO pattern and you should [check](https://www.baeldung.com/java-immutable-object) it!

## When Lombok is a good fit

Lombok can make Java data classes and logging setup more concise. Agree on the annotations your team will use and configure every developer’s IDE and build consistently. Spring Initializr can also add Lombok to a generated project.

See the [Project Lombok site](https://projectlombok.org/) and its [feature documentation](https://projectlombok.org/features/all) for details.
