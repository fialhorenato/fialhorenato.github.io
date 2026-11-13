---
title: "Learn the SOLID Principles with Java Examples"
tags:
  - Java
  - SOLID
  - Software design
description: Learn the five SOLID design principles through Java examples covering responsibility, extension, substitution, interfaces, and dependencies.
last_modified_at: 2026-11-13
layout: single
---

This guide explains the five SOLID principles—Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion—with Java examples. Treat them as design heuristics: apply them when they make a system easier to change and understand, rather than as rules that require extra abstractions everywhere.

## What is SOLID?

**S.O.L.I.D** stands for:

[**S**ingle Responsibility Principle](#single-responsibility-principle)

[**O**pen Closed Principle](#open-closed-principle)

[**L**iskov Substitution Principle](#liskov-substitution-principle)

[**I**nterface Segregation Principle](#interface-segregation-principle)

[**D**ependency Inversion Principle](#dependency-inversion-principle)

Design principles can help a team write software that is easier to maintain and work on together.

## Single Responsibility Principle

A class should have only one responsibility.

It helps into onboarding new members into the code, as well to test, maintain and grow our codebase.

### Example

Imagine that you have a `UserService` that is like this:

```java
class UserService {
    
    public void createUser() {
        // Create our user here
    }
    
    public User findById(UUID id) {
        // Return our user
    }
    
    private void sendAppNotification() {
        // Send an app notification
    }

    private void sendEmail() {
        // Send an email
    }
}
```

What happens if the notification requirements change? If the class also handles email, push notifications, and SMS, those responsibilities can change for different reasons.

We can separate the notification responsibility into a `NotificationService` that handles communication channels.

```java
class UserService {

    private final NotificationService notificationService;
    
    public void createUser() {
        // Create our user here
    }
    
    public User findById(UUID id) {
        // Return our user
    }
}
```

```java
class NotificationService {
    public void sendSms() {
        // Send SMS
    }

    public void sendPushNotification() {
        // Send push
    }

    public void sendEmail() {
        // Send email
    }
}
```

There are several ways to structure this example. The key idea is to separate responsibilities that change for different reasons.

## Open/Closed Principle

Software entities (classes, modules, and functions) should be open to extension and closed to modification.

## Example

Suppose we have a `CoffeeApp` class:

```java
public class CoffeeApp {
    public void brewSimpleCoffee() {
        // Put water
        // Put coffee powder
    }

    public void brewPremiumCoffee() {
        // Get the bean
        // Grind the bean
        // Put water
    }
}
```

Imagine that everytime our system needs to support a new type of coffee, we must change the Machine in order to add a new type.

Lets use of simple abstraction and polymorphism to improve this

```java
public class CoffeeApp {
    public static void greet(CoffeeMachine coffeeMachine) {
        coffeeMachine.brewCoffee(ESPRESSO);
    }
}

interface CoffeeMachine {
    Coffee brewCoffee(CoffeeSelection selection);
}

public class BasicCoffeeMachine implements CoffeeMachine {
    private BrewingUnit brewingUnit;

    @Override
    public Coffee brewCoffee(CoffeeSelection selection) {
        brewFilterCoffee();
    }

    private brewFilterCoffee() {
        brewingUnit.brew();
    }
}

public class PremiumCoffeeMachine implements CoffeeMachine {
    private Grinder grinder;
    private BrewingUnit brewingUnit;

    @Override
    public Coffee brewCoffee(CoffeeSelection selection) {
    switch(selection) {
        case ESPRESSO:
            return brewEspresso();
        case FILTER_COFFEE:
        default:
            return brewFilterCoffee();
        }
    }

    private brewEspresso() {
        grinder.grind()
        brewingUnit.brew();
    }

    private brewFilterCoffee() {
        brewingUnit.brew();
    }
}
``` 

Now that class is opened for extension (ItalianMachine, ColombianMachine, FrenchPressMachine) and closed for modification (won’t have a method with a different logic being added every time a new machine is added to the app).

## Liskov Substitution Principle

A class can be replaced by its subclass in all practical usage scenarios, meaning that you should use inheritance only for substitutability.

## Example

Using an Animal example

```java
interface Animal {
    void fly();
    void swim();
}

public class Dog implements Animal {
    // A dog can swim
    @Override
    public void swim() {
        // Swim
    }

    // But a dog cannot fly
    @Override
    public void fly() {
        throw IllegalStateException();
    }
}

public class Hawk implements Animal {
    // A hawk cannot swim
    @Override
    public void swim() {
        throw IllegalStateException();
    }

    // But a hawk can fly
    @Override
    public void fly() {
       // Fly
    }
}
```

Even though, both a `Dog` and a `Hawk` are animals, we can break up the inheritance to follow up this principle

```java
interface Animal {
    void swim();
}

interface Bird {
    void fly();
}

public class Dog implements Animal {
    // A dog can swim
    @Override
    public void swim() {
        // Swim
    }
}

public class Hawk implements Bird {
    // A hawk can fly
    @Override
    public void fly() {
       // Fly
    }
}
```

## Interface Segregation Principle

A client shouldn’t be forced to implement an interface that it doesn’t use.

## Example

Thinking about the last example, even though a Dog can only swim, some `Animal`s can swim and fly.

Isn't easier if we just implement the interfaces like this

```java
interface Swimmer {
    void swim();
}

interface Bird {
    void fly();
}

public class Dog implements Swimmer {
    // A dog can swim
    @Override
    public void swim() {
        // Swim
    }
}

public class Hawk implements Bird {
    // A hawk can fly
    @Override
    public void fly() {
       // Fly
    }
}

public class Duck implements Swimmer, Bird {
    // A duck can fly
    @Override
    public void fly() {
       // Fly
    }

    // A duck can swim
    @Override
    public void swim() {
        // Swim
    }
}
```

## Dependency Inversion Principle

We should invert the classic dependency between higher level modules and lower level modules, by abstracting their interaction.

### Example

Let's say we have some implementations over a database

```java
public class PersonService {
    private final PersonRepository personRepository;

    public PersonService(PersonRepository personRepository) {
        this.personRepository = personRepository;
    }
}

interface PersonRepository {
    Person findById(UUID id);
    Person create(UUID id, String name);
}

public class LocalRepository implements PersonRepository {
    private Map<UUID, Person> repository;

    // Implement the methods
}

public class DatabaseRepository implements PersonRepository {
    // Hibernate entity manager to handle the communication towards the Database.
    private EntityManager entityManager;

    // Implement the methods
}
```

With this design, the high-level `PersonService` depends on the `PersonRepository` abstraction. The implementation can be replaced without changing the service’s core logic.

For example, you can replace the persistence implementation without making the service depend directly on Hibernate details.

---


In case if you have any questions or suggestions, feel free to send me a [message](/contact)
