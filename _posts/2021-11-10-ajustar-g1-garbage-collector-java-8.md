---
title: "Garbage Collector G1 no Java 8: Ajustes e Concessões"
description: "Revise conceitos do G1 GC no Java 8, configurações de heap e pausas e por que os parâmetros da JVM devem ser medidos na sua aplicação."
date: 2021-11-10
lang: pt-BR
permalink: /blog/ajustar-g1-garbage-collector-java-8
translation_url: "/blog/tune-your-jvm-gc"
tags:
  - Desenvolvimento de Software
last_modified_at: 2026-11-15
layout: single
toc: true
locale: pt_BR
translation_label: "Read this article in English"
---

*Read this post in English: [Java 8 G1 Garbage Collection: Tuning Notes and Trade-Offs](/blog/tune-your-jvm-gc).* 

Este artigo reúne anotações sobre ajustes do garbage collector G1 em um serviço Java 8. Aborda metas de pausa, dimensionamento do heap e algumas opções que vale a pena entender.

**Contexto histórico:** os padrões da JVM e o comportamento do garbage collector variam conforme a versão do JDK e a carga de trabalho. Considere estas observações como referências da época do Java 8, não como parâmetros para copiar sem análise. Meça a aplicação no JDK de destino antes de alterar opções da JVM.

## Garbage collection do G1

## Minor GC, Major GC e Full GC

O Micrometer pode expor métricas de garbage collection para serviços JVM. Os nomes exatos dos eventos e o comportamento do collector dependem do JDK e do collector; a terminologia resumida abaixo reflete discussões antigas de HotSpot e Java 8.

### Minor GC

- Em geral, recupera regiões da geração jovem.
- As pausas de coleta do G1 interrompem as threads da aplicação, embora a marcação concorrente possa ocorrer em paralelo com elas.

### Major GC

- “Major GC” é um termo informal usado com frequência para atividades de coleta que envolvem memória da geração antiga; não é um nome universalmente preciso para eventos do G1.

### Full GC

- Uma Full GC recupera o heap e costuma ser um evento de alto impacto. Investigue a causa em vez de presumir que seja rotineira.

## Ajustar o heap e o tempo de pausa

### Definir deliberadamente o tamanho inicial e máximo do heap

Escolher o tamanho inicial e máximo do heap depende da carga de trabalho e do dimensionamento do contêiner. Igualar `-XX:InitialRAMPercentage` e `-XX:MaxRAMPercentage` pode evitar expansão posterior do heap, mas também reserva mais memória no início e deixa menos espaço para memória nativa e outros processos. Meça a inicialização, o uso de memória e as pausas sob uma carga realista antes de fixar os valores.

### Definir uma meta de pausa

`-XX:MaxGCPauseMillis` define uma meta de pausa, não um limite máximo garantido. O G1 usa esse valor como um dos fatores ao escolher o trabalho de coleta; uma meta mais agressiva pode afetar a vazão e não garante que todas as pausas ficarão abaixo dela.

### Deixar o G1 dimensionar a geração jovem

Evite fixar o tamanho da geração jovem (por meio de opções como `-Xmn` ou `-XX:NewRatio`).

O G1 ajusta a geração jovem com base nas metas de pausa. Valores fixos podem restringir essa adaptação; evite ajustá-los sem medições e uma justificativa específica.

### Remover opções obsoletas do collector

Remova opções de collectors que já não são usados. Algumas podem ser ignoradas ou entrar em conflito com o collector selecionado; confira a documentação de logging unificado e das opções do JDK de destino.

### Considerar a deduplicação de strings

Em configurações compatíveis do G1, `-XX:+UseStringDeduplication` pode reduzir a memória ocupada por strings duplicadas, ao custo de trabalho adicional. Primeiro faça o perfil da aplicação e consulte a documentação do JDK de destino.

## Opções da JVM para conhecer

| Opção da JVM | O que controla | Observação prática |
| --- | --- | --- |
| `-XX:MaxGCPauseMillis` | Meta de pausa do G1 | É uma meta, não uma garantia; o padrão depende da versão do JDK. |
| `-XX:G1HeapRegionSize` | Tamanho das regiões no heap G1 | Em geral, a JVM escolhe esse valor automaticamente. Só altere após medir. |
| `-XX:GCTimeRatio` | Proporção desejada entre tempo de GC e tempo da aplicação | É um fator de ajuste, não uma promessa de percentual fixo. |
| `-XX:ParallelGCThreads` | Threads para fases com interrupção da aplicação | Os padrões levam em conta os processadores disponíveis e podem considerar contêineres. |
| `-XX:ConcGCThreads` | Threads para marcação concorrente | Os padrões variam; mudar esse valor troca disponibilidade de CPU por progresso do GC. |
| `-XX:InitiatingHeapOccupancyPercent` | Limite de ocupação que pode iniciar a marcação concorrente | O IHOP adaptativo pode ajustar o comportamento; consulte o JDK de destino. |
| `-XX:G1NewSizePercent`, `-XX:G1MaxNewSizePercent` | Limites para o tamanho da geração jovem | Evite fixá-los sem evidências; o G1 ajusta o tamanho para atender às metas. |
| `-XX:G1OldCSetRegionThresholdPercent` | Limite de regiões antigas selecionadas numa coleta mista | Verifique a disponibilidade e o significado nessa versão exata do JDK. |
| `-XX:G1ReservePercent` | Capacidade reservada para reduzir risco de falha na evacuação | Aumentar o valor reduz o heap disponível para a aplicação; padrão e orientação variam por versão. |
