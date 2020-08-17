---
title: Stop writing boilerplate code in Java with Project Lombok
tags: Java Technology
style: fill
color: dark
description: Stop writing getters, setters, toString and other boilerplate code in Java POJOs
layout: post
---

How many time did you already lose writing boilerplate code in Java? Or generating those in your IDE?

A simple POJO has as least *getters*, *setters*, *constructors*, *toString*, *equals*, *hashCode* and that's a lot of code!

Other programming languages such as Scala and Kotlin provides dynamic access to properties without no extra boilerplate code, but there's a solution for Java? **Yes**

# Project Lombok
That's how project Lombok describes themselves:

> Project Lombok is a java library that automatically plugs into your editor and build tools, spicing up your java.
> Never write another getter or equals method again, with one annotation your class has a fully featured builder, Automate your logging variables, and much more.

Lombok is all based in annotations and generates all the boilerplate code in compile-time, which makes the code more readable, less error-prone and makes the development way more productive!

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
    Person person = (Person) p;
    return name == person.name &&
        age == person.age;
  }

  @Override
  public int hashCode() {
    return Objects.hash(name, age, chassisCode);
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

The [@Value](https://projectlombok.org/features/Value) annotation makes immutable classes very easy!

>@Value is the immutable variant of @Data; all fields are made private and final by default, and setters are not generated. The class itself is also made final by default, because immutability is not something that can be forced onto a subclass. Like @Data, useful toString(), equals() and hashCode() methods are also generated, each field gets a getter method, and a constructor that covers every argument (except final fields that are initialized in the field declaration) is also generated.

I'll write a post in the future of the pros and cons for Immutable classes in Java, but it's a great POJO pattern and you should [check](https://www.baeldung.com/java-immutable-object) it!

## Conclusion

Project lombok is one of your best friends when writing Java POJO's and even classes, and even Spring Boot suggests it as one of the dependencies on [Spring Initialzr](http://www.start.spring.io).

Please check the [Lombok Project](https://projectlombok.org/) and it's [documentation](https://projectlombok.org/features/all) page to know more of this powerful tool.