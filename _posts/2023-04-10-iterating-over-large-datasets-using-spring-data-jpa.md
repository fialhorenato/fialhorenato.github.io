---
title: Iterating over large datasets using Spring Data JPA
tags: Java Development Spring
style: fill
color: warning
description: Findings on learning how to iterate over large datasets using Spring Data JPA
layout: post
---

In this post, I'll explain some learnings on how to iterate through large data sets retrieved with Spring Data JPA.

## Pagination

When iterating over large datasets from a Database, the first and easiest idea is to use pagination to fetch and process the data in bulks, but not a lot of developers know that there is 2 different ways of
fetching data on Spring Data JPA and what is the difference between them.

First, lets explain the `Slice`.

For the examples provided in this post, i'll use a ficticious `Person` entity.

```java
@Entity
@Value
public class Person {

    @Id
    UUID id;

    String firstName;
    String lastName;
}
```


### Slice

In order to create a query that finds all entities of Person paginated, we need to create a JpaRepository that receives a `Pageable` as a parameter and return a `Slice` as a return type.

```java
@Repository
public interface PersonRepository extends JpaRepository<Person, UUID> {
    Slice<Person> findAllBy(Pageable page);
}
```

The return type of the method `findAllBy` is of `Slice<Person>`, which returns the first batch of entities to be processed based on the values provided by the `Pageable`.

The `Slice` interface exposes a `hasNext()` method that allows us to know if there is another page of entities or not. As well, the interface exposes the `nextPageable()` method that returns
the next `Pageable` object that we need to query for the next page.

Saying this, a good way to iterate and call a function `doSomething(Person p)` over every person fecthed is:

```java
void processAll() {
    Slice<Person> slice = repository.findAllBy(PageRequest.of(0, BATCH_SIZE));
    List<Person> persons = slice.getContent();
    persons.forEach(this::doSomething);

    while(slice.hasNext()) {
        slice = repository.findAllBy(slice.nextPageable());
        slice
            .getContent()
            .forEach(this::doSomething);
    }
}
```

If we debug the queries executed by the method above, Hibernate will log this:


```java
[main] DEBUG org.hibernate.SQL - select person0_.id as id1_0_, person0_.first_name as first_na2_0_, person0_.last_name as last_nam3_0_ from person person0_ limit ?
[main] DEBUG org.hibernate.SQL - select person0_.id as id1_0_, person0_.first_name as first_na2_0_, person0_.last_name as last_nam3_0_ from person person0_ limit ? offset ?
[main] DEBUG org.hibernate.SQL - select person0_.id as id1_0_, person0_.first_name as first_na2_0_, person0_.last_name as last_nam3_0_ from person person0_ limit ? offset ?
```

### Page

Another option aside `Slice`, there is the `Page` interface that we can use as a return type of the query.

```java
@Repository
public interface PersonRepository extends JpaRepository<Person, UUID> {
    Slice<Person> findAllBy(Pageable page);
    Page<Person> findAllBy(Pageable page);
}
```

The `Page` interface extends the `Slice` interface and adds two other methods to it: `getTotalPages()` and `getTotalElements()`.

It is an extra information that helps the client to know how many more pages are needed in order to fetch all elements of the dataset at the cost of an extra query on the DB that can
take some time.

```java
void processAll() {
    Page<Person> page = repository.findAllBy(PageRequest.of(0, BATCH_SIZE));
    List<Person> persons = page.getContent();
    persons.forEach(this::doSomething);

    while(page.hasNext()) {
        page = repository.findAllBy(page.nextPageable());
        page
            .getContent()
            .forEach(this::doSomething);
    }
}
```

```java
[main] DEBUG org.hibernate.SQL - select person0_.id as id1_0_, person0_.first_name as first_na2_0_, person0_.last_name as last_nam3_0_ from person person0_ limit ?
[main] DEBUG org.hibernate.SQL - select count(person0_.id) as col_0_0_ from person person0_
[main] DEBUG org.hibernate.SQL - select person0_.id as id1_0_, person0_.first_name as first_na2_0_, person0_.last_name as last_nam3_0_ from person person0_ limit ? offset ?
[main] DEBUG org.hibernate.SQL - select count(person0_.id) as col_0_0_ from person person0_
[main] DEBUG org.hibernate.SQL - select person0_.id as id1_0_, person0_.first_name as first_na2_0_, person0_.last_name as last_nam3_0_ from person person0_ limit ? offset ?
[main] DEBUG org.hibernate.SQL - select count(person0_.id) as col_0_0_ from person person0_
```

Since `Page` is clearly less performant than the `Slice`, we should only use page when we need to know the total number of entities.


## Streams (Java 8+)

In Spring Data JPA there is another option which is return a stream of elements, but as a result, we can only process the entities one by one.

As a leverage, we don´t load all the entities into memory at the same time.

```java
@Repository
public interface PersonRepository extends JpaRepository<Person, UUID> {
    Slice<Person> findAllBy(Pageable page);
    Page<Person> findAllBy(Pageable page);
    Stream<Person> findAllBy();
}
```

Spring Data require us to manually close the stream created by the Spring Data JPA with a try-with-resource block, and as well, use a `@Transactional(readOnly=true)` annotation to the method called by the repository.

```java
private final EntityManager entityManager;

@Transactional(readOnly = true)
public void processAll() {
    try (Stream<Person> persons = repository.findAllBy()) {
        persons
            .peek(entityManager::detach)
            .forEach(this::doSomething);
    }
}
```

## Conclusion

We should always use:

- `Slice` if the number of entities is not relevant to us, and it is the most performance way of fecthing this data
- `Page` if the number of entities is relevant, but at the cost of an extra query
- `Stream` if we do not have a lot of memory and a sequential processing of the dataset is not a problem