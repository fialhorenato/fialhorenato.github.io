---
title: "Spring Data JPA: Page, Slice, or Stream for Large Datasets"
tags:
  - Software Development
description: "Compare Spring Data JPA Page, Slice, and Stream for large result sets, including count queries, batching, memory use, and resource handling."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
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

To fetch people in batches, declare a repository method that accepts a `Pageable` and returns a `Slice<Person>`.

```java
@Repository
public interface PersonRepository extends JpaRepository<Person, UUID> {
    Slice<Person> findAllBy(Pageable page);
}
```

`Slice<Person>` contains the current batch and paging metadata, based on the supplied `Pageable`.

Use `hasNext()` to check whether another batch exists and `nextPageable()` to request it.

For example, the following loop processes each batch before fetching the next one:

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

Use `Page<Person>` when the caller also needs total counts or page counts.

```java
@Repository
public interface PersonRepository extends JpaRepository<Person, UUID> {
    Page<Person> findAllBy(Pageable page);
}
```

For a `Page` query, declare the repository method with `Page<Person>` as its return type. `Page` extends `Slice` and adds `getTotalPages()` and `getTotalElements()`.

The total count helps a client display the number of results or pages, but computing it can add database work. Spring Data may optimize or skip a count in some cases; inspect generated queries for your query and version.

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

A repository can also return a `Stream<Person>` for sequential processing. This can avoid collecting every result into one application-side list, but it does not automatically guarantee incremental fetching.

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

Choose based on what the caller needs:

- Use `Slice` for batches and a “has next” indicator without requesting total counts.
- Use `Page` when the client needs total elements or pages, while checking the cost of count queries.
- Use `Stream` when provider and driver behavior support your memory goals; close it promptly and consume it inside a transaction.

For very large or frequently changing datasets, also consider keyset scrolling, bounded persistence-context growth, stable ordering, transaction duration, and database indexes. Benchmark the generated SQL and memory behavior with representative data.
