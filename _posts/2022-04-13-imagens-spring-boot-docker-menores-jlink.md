---
title: "Como Criar Imagens Docker Menores para Spring Boot com jlink"
description: "Use jdeps e jlink para criar um runtime Java personalizado para uma imagem Spring Boot, com exemplo histórico do Java 17 e ressalvas de compatibilidade."
date: 2022-04-13
lang: pt
permalink: /blog/imagens-spring-boot-docker-menores-jlink
translation_url: /blog/creating-slim-spring-boot-images
tags:
  - Desenvolvimento de Software
last_modified_at: 2026-11-15
layout: single
toc: true
---

*Read this post in English: [Build Smaller Spring Boot Docker Images with jlink](/blog/creating-slim-spring-boot-images).* 

Este passo a passo de 2022 mostra como usei `jdeps` e `jlink` para criar um runtime Java menor para uma imagem Docker com Spring Boot. Os nomes das imagens e os comandos são da época do Java 17; revise a imagem-base, a versão do Java e a lista de módulos para a aplicação atual antes de adotar o exemplo.

`jdeps` e `jlink` estão disponíveis desde o Java 9. Eles ajudam a criar um runtime personalizado com os módulos selecionados do JDK, o que pode reduzir o tamanho da imagem de uma aplicação Java. O resultado depende da aplicação, das dependências, da imagem-base e do processo de build; meça a imagem final e teste cuidadosamente o runtime.

## Inspecionar as dependências da aplicação

Use uma versão do JDK compatível com a aplicação e construa o runtime com a mesma versão principal do JDK. Os comandos abaixo refletem uma configuração Java 17 de 2022.

Comece inspecionando a aplicação com `jdeps`:

```shell
$ jdeps --list-deps --ignore-missing-deps your-fat-jar.jar
   java.base
   java.logging
```

Se a saída parecer incompleta, isso é esperado num arquivo executável do Spring Boot: as dependências ficam dentro do diretório aninhado `BOOT-INF/lib`. Uma execução básica do `jdeps` no arquivo externo pode não analisar recursivamente todas elas.

Extraia o arquivo e analise individualmente as classes da aplicação e os JARs de dependências, ou use um fluxo de análise de dependências em tempo de build. Em seguida, valide a lista de módulos executando a aplicação com o runtime vinculado e exercitando caminhos que carreguem classes por reflexão. Uma `ClassNotFoundException` em produção é um sinal tardio; inclua testes de integração.

Nos meus projetos anteriores, estes módulos eram pontos de partida comuns, não uma lista garantida para toda aplicação Spring Boot:

```
java.compiler
java.logging
java.sql
java.rmi
java.naming
java.management
java.instrument
java.security.jgss
java.net.http
jdk.httpserver
jdk.naming.dns
```

Considere a lista um ponto de partida de uma aplicação, não um conjunto de módulos reutilizável. Descubra quais módulos sua aplicação e bibliotecas precisam e repita a análise sempre que as dependências mudarem.

## Criar um runtime Java personalizado com jlink

É possível usar o `jlink` localmente para criar um JRE personalizado. O comando é semelhante a este:

```shell
jlink \
    --module-path "$JAVA_HOME/jmods" \
    --add-modules [módulos Java necessários à aplicação, separados por vírgula] \
    --verbose \
    --strip-debug \
    --compress 2 \
    --no-header-files \
    --no-man-pages \
    --output /opt/jre-minimal
```

Resumo das opções:

```
--module-path <caminho>            Caminho dos módulos.
                                    Se omitido, usa o diretório jmods do JDK, caso exista.
                                    Se indicado sem java.base, o diretório jmods do JDK
                                    pode ser acrescentado, caso exista.

--verbose                           Habilita rastreamento detalhado
--strip-debug                       Remove informações de depuração
--compress=<0|1|2>                  Habilita compressão de recursos:
                                      0: sem compressão
                                      1: compartilhamento de strings constantes
                                      2: ZIP
--no-header-files                   Exclui arquivos de cabeçalho
--no-man-pages                      Exclui páginas de manual
--output <caminho>                  Diretório de saída
```

Para ver as opções aceitas pelo JDK instalado, execute `jlink --help`.

## Empacotar o runtime com uma aplicação Spring Boot

Este Dockerfile ilustrativo com múltiplas etapas usa nomes de imagens da época do Java 17. Atualize as imagens-base para versões suportadas e compatíveis com o JDK de destino antes de usá-lo.

```Dockerfile
# Criar um runtime mínimo com jlink
FROM openjdk:17 AS builder
USER root
RUN jlink \
    --module-path "$JAVA_HOME/jmods" \
    --add-modules java.compiler,java.sql,java.naming,java.management,java.instrument,java.rmi,java.desktop,jdk.internal.vm.compiler.management,java.xml.crypto,java.scripting,java.security.jgss,jdk.httpserver,java.net.http,jdk.naming.dns,jdk.crypto.cryptoki,jdk.unsupported \
    --verbose \
    --strip-debug \
    --compress 2 \
    --no-header-files \
    --no-man-pages \
    --output /opt/jre-minimal
USER app

# Montar a imagem da aplicação sobre uma imagem compatível
FROM bitnami/minideb:bullseye

# Adicionar o runtime personalizado
COPY --from=builder /opt/jre-minimal $JAVA_HOME

# Copiar o JAR produzido pelo Gradle
# COPY build/libs/app.jar app.jar

# Ou copiar o JAR produzido pelo Maven
# COPY target/app.jar app.jar

ENTRYPOINT ["java","-jar","/app.jar"]
```

## Medir o resultado no tamanho da imagem

No meu exemplo de 2022, a imagem resultante ficou cerca de 200 MB menor que a original. O resultado varia conforme a aplicação e a imagem-base; registries também podem deduplicar camadas compartilhadas. Meça o tamanho armazenado e transferido real, em vez de presumir a mesma economia.
