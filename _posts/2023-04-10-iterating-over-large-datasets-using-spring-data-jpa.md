---
title: "Process Large Datasets with Spring Data JPA: Page, Slice, or Stream"
tags:
  - Software Development
description: Compare Page, Slice, and Stream in Spring Data JPA when processing large result sets.
last_modified_at: 2026-11-13
layout: single
---

When processing a large Spring Data JPA result set, the choice between `Slice`, `Page`, and `Stream` affects count queries, resource lifetime, and memory use. This guide compares the trade-offs and shows when each return type can fit.

## Pagination

Pagination fetches results in batches. Spring Data JPA’s `Slice` and `Page` both represent a batch, but a `Page` also exposes total counts, which may require an additional count query.

First, consider `Slice`.

The examples use a simple `Person` entity.

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
    Page<Person> findAllBy(Pageable page);
}
```

For a `Page` query, declare the repository method with `Page<Person>` as its return type. `Page` extends `Slice` and adds `getTotalPages()` and `getTotalElements()`.

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

The count query can add database work, so use `Page` when the total count or number of pages is useful to the caller. If the caller only needs to know whether another batch exists, `Slice` avoids requesting that total.


## Streams (Java 8+)

In Spring Data JPA there is another option which is return a stream of elements, but as a result, we can only process the entities one by one.

This can avoid collecting every result into a list at once, although actual fetching and memory behavior depends on the persistence provider and JDBC driver.

```java
@Repository
public interface PersonRepository extends JpaRepository<Person, UUID> {
    Stream<Person> findAllBy();
}
```

Close the stream with try-with-resources and consume it inside a transaction. A `Stream` does not by itself guarantee incremental fetching; actual memory use depends on the JPA provider, JDBC driver, and fetch-size configuration. See the [Spring Data JPA reference](https://docs.spring.io/spring-data/jpa/reference/repositories/query-return-types-reference.html).

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

- `Slice` when the caller needs batches and a “has next” indicator, but not a total count.
- `Page` when the caller needs total elements or pages, accepting the possible cost of a count query.
- `Stream` when streaming fits the persistence provider and driver behavior; close it promptly and process it inside a transaction.
