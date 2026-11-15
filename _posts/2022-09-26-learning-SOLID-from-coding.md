---
title: "The SOLID Principles Explained with Java Examples"
tags:
  - Software Development
description: "Learn the five SOLID object-oriented design principles through Java examples and understand the trade-offs behind applying them."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
header:
  image: /images/post-covers/learning-SOLID-from-coding.svg
  image_description: "The SOLID Principles Explained with Java Examples"
---

This guide explains the five SOLID principles—Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion—with Java examples. Treat them as design heuristics: apply them when they make a system easier to change and understand, rather than as rules that require extra abstractions everywhere.

## The five principles at a glance

| Principle | Short version |
| --- | --- |
| [Single Responsibility](#single-responsibility-principle) | Keep a module focused around a cohesive responsibility. |
| [Open/Closed](#openclosed-principle) | Make expected variation possible without repeatedly changing stable code. |
| [Liskov Substitution](#liskov-substitution-principle) | Subtypes should preserve the behavior callers expect from the base type. |
| [Interface Segregation](#interface-segregation-principle) | Keep interfaces focused on the needs of their clients. |
| [Dependency Inversion](#dependency-inversion-principle) | Let high-level policy depend on abstractions, not low-level details. |

These are design heuristics for making change safer and code easier to understand. The examples below show one way to apply each idea; they are not templates to copy without considering the problem.

## Single Responsibility Principle

A class should have only one responsibility.

A well-defined responsibility can make a class easier to understand, test, and change. The useful boundary depends on the reasons the behavior changes; splitting every method into its own class is not the goal.

### Example

Suppose a `UserService` creates and looks up users, but also sends notifications:

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

If notification behavior changes independently, it may belong in a separate collaborator:

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

### Example: vary behavior behind an interface

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

If each new coffee type requires editing the same class, the class accumulates conditionals and reasons to change. An abstraction can move variation behind a stable interface, although this is useful only when the variation is real and expected.

```java
public class CoffeeApp {
    public static void serve(CoffeeMachine coffeeMachine) {
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

The example introduces a `CoffeeMachine` abstraction so the application can work with different implementations. The principle does not mean code can never change; it means stable policy should not need repeated edits for every expected variation. Add an abstraction when the variations justify its cost.

## Liskov Substitution Principle

Code that accepts a base type should continue to work when given a subtype. A subtype should preserve the promises and constraints of the base type rather than surprising callers with unsupported operations.

### Example: model behavior contracts

An interface that requires every animal to fly and swim forces some implementations to reject valid calls:

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

Separate capabilities so a type only promises behaviors it can support:

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

### Example: split capabilities

Small capability interfaces let clients depend only on the operations they use:

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

### Example: depend on a repository contract

The service depends on a repository contract rather than a concrete storage technology:

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


## Applying SOLID in practice

SOLID is a set of design heuristics, not a checklist that every class must satisfy in isolation. Start with the simplest design that meets today’s requirements, then introduce abstractions when change, duplication, or testing pain provides a reason. Evaluate the result by whether the code is easier to understand and safely modify.
