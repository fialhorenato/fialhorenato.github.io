---
title: "Como Corrigir Erros npm EXDEV em Contêineres Docker"
description: "Entenda por que o npm pode gerar erros EXDEV em builds Docker e conheça uma solução histórica e práticas mais seguras."
date: 2021-08-12
lang: pt-BR
permalink: /blog/corrigir-exdev-npm-docker
translation_url: "/blog/learnings-docker-node"
tags:
  - Desenvolvimento de Software
last_modified_at: 2026-11-15
layout: single
locale: pt_BR
translation_label: "Read this article in English"
header:
  image: /images/post-covers/learnings-docker-node.svg
  image_description: "Como Corrigir Erros npm EXDEV em Contêineres Docker"
---

*Read this post in English: [Fixing npm EXDEV Errors in Docker Containers](/blog/learnings-docker-node).* 

Ao trabalhar em um projeto, usei um Dockerfile para instalar dependências e compilar uma aplicação Angular 9. Este artigo registra um erro `EXDEV` que encontrei e a solução temporária que tentei. O comportamento do Docker e do npm varia conforme as versões e a configuração do build; trate o exemplo como uma situação de diagnóstico, não como uma correção universal.

## O que significa o erro npm EXDEV

O erro `EXDEV` indica que uma operação atravessou o limite entre sistemas de arquivos. Ele não é específico do Docker; a causa exata depende do npm, do sistema de arquivos e de como as camadas da imagem são usadas. No meu caso, apareceu ao modificar arquivos relacionados ao npm durante o build do contêiner.

Mais especificamente, o erro pode ocorrer quando o npm tenta renomear um arquivo entre sistemas de arquivos. A operação de renomeação é atômica apenas dentro do mesmo sistema de arquivos; ao atravessar esse limite, pode ocorrer `EXDEV` (link entre dispositivos).

Uma solução temporária discutida nesta [issue do npm](https://github.com/npm/npm/issues/9863) era mover o diretório antes da instalação:

```
RUN mv ./node_modules ./node_modules.tmp \
  && mv ./node_modules.tmp ./node_modules \
  && npm install
```

Essa solução contornou o problema no ambiente específico que encontrei; não é uma correção geral para Docker. Sistemas de arquivos de contêiner usam camadas e o comportamento de renomeação varia entre sistemas e montagens. Antes de adotar a solução, reproduza o erro nas versões atuais do Node.js e npm e verifique em quais sistemas de arquivos estão os caminhos envolvidos. Prefira um fluxo de instalação e build suportado que produza as dependências na mesma camada de sistema de arquivos em que serão usadas.

## Mantenha os builds de contêiner reproduzíveis

Contêineres são substituíveis; portanto, as dependências de build devem ser reproduzidas a partir do código-fonte e dos arquivos de lock. Gere os artefatos necessários durante o build da imagem ou inclua-os no contexto de build. Passe segredos em tempo de execução por um mecanismo apropriado de gerenciamento de segredos; não os grave na imagem.
