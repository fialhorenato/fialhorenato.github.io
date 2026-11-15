---
title: "Como Reduzir Código Boilerplate em Java com Project Lombok"
description: "Veja como o Project Lombok gera métodos comuns em Java, como configurar o suporte na IDE e quais concessões considerar."
date: 2020-08-17
lang: pt
permalink: /blog/reduzir-boilerplate-java-lombok
translation_url: /blog/stop-writing-boilerplate-code-in-java
tags:
  - Desenvolvimento de Software
last_modified_at: 2026-11-15
layout: single
---

*Read this post in English: [Reduce Java Boilerplate with Project Lombok](/blog/stop-writing-boilerplate-code-in-java).* 

Você já passou um tempo escrevendo — ou gerando pela IDE — os mesmos getters, setters, construtores e métodos auxiliares em Java? Uma simples classe de dados pode exigir getters, setters, construtores, `toString`, `equals` e `hashCode`.

Linguagens como Kotlin e Scala reduzem parte desse código repetitivo. Quem desenvolve em Java também pode usar o Project Lombok, que gera métodos comuns a partir de anotações.

## O que é o Project Lombok?

O Lombok se descreve como uma biblioteca Java que se integra a editores e ferramentas de build para gerar código comum a partir de anotações (paráfrase do [site do Project Lombok](https://projectlombok.org/)).

O Lombok usa anotações e gera código durante a compilação. Isso pode encurtar os arquivos-fonte, mas a equipe deve ponderar essa conveniência diante das configurações adicionais necessárias na IDE e no build.

![Ilustração de anotações distribuídas pelo código Java](/images/annotations-everywhere.jpg "Anotações em toda parte")

Para usar o Lombok com conforto, configure o processamento de anotações e o suporte da IDE para as ferramentas do projeto. A configuração de build é a fonte de verdade; consulte o [guia de configuração atual](https://projectlombok.org/setup/).

- Consulte as instruções para [Eclipse](https://projectlombok.org/setup/eclipse).
- Para o IntelliJ, instale o [plugin do Lombok](https://plugins.jetbrains.com/plugin/6317-lombok).
- Consulte as instruções para [NetBeans](https://projectlombok.org/setup/netbeans).

## Getters, setters, `toString`, `equals` e `hashCode`

Este código:

```java
public class Person{
  private String name;
  private int age;

  public String getName(){ return name; }
  public void setName(String name){ this.name = name; }
  public int getAge(){ return age; }
  public void setAge(int age){ this.age = age; }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Person person = (Person) o;
    return name == person.name && age == person.age;
  }
  @Override
  public int hashCode() { return Objects.hash(name, age); }
  @Override
  public String toString() {
    return "Person{" + "name=" + name + ", age=" + age + '}';
  }
}
```

Pode ser reduzido a:

```java
@Data
public class Person{
  private String name;
  private int age;
}
```

![Animação ilustrando código gerado](/images/magic.gif "Código gerado")

A anotação [`@Data`](https://projectlombok.org/features/Data) reúne `@ToString`, `@EqualsAndHashCode`, `@Getter` para todos os campos, `@Setter` para campos não finais e `@RequiredArgsConstructor`.

## Reduzir código repetitivo de logging

O Lombok ajuda a configurar logging com a biblioteca escolhida para o projeto. Há suporte para Log4j, Log4j2, SLF4J, Commons Logging e outras. Consulte a página da anotação [`@Log`](https://projectlombok.org/features/log).

## Classes imutáveis e builders

A anotação [`@Value`](https://projectlombok.org/features/Value) pode deixar classes imutáveis mais concisas. Ela é a variante imutável de `@Data`: os campos são privados e finais por padrão, setters não são gerados, e o Lombok gera métodos como `toString()`, `equals()`, `hashCode()`, getters e um construtor com todos os argumentos. Veja a [documentação oficial de `@Value`](https://projectlombok.org/features/Value) para mais detalhes.

Ainda pretendo escrever sobre as vantagens e desvantagens de classes imutáveis em Java. Elas são um bom padrão para POJOs; veja também este artigo sobre [objetos imutáveis em Java](https://www.baeldung.com/java-immutable-object).

## Quando o Lombok pode ser uma boa escolha

O Lombok pode deixar classes de dados e configurações de logging em Java mais concisas. Combine com a equipe quais anotações serão usadas e configure de forma consistente as IDEs e o build de cada pessoa. O Spring Initializr também pode incluir o Lombok em um projeto gerado.

Consulte o [site do Project Lombok](https://projectlombok.org/) e a [documentação dos recursos](https://projectlombok.org/features/all).

O Lombok reduz o código-fonte, mas métodos gerados ficam menos visíveis durante revisões e podem depender da configuração da IDE e do build. Combine com a equipe quais anotações são aceitáveis, confira o comportamento gerado e considere Java records para tipos simples e imutáveis quando forem adequados.
