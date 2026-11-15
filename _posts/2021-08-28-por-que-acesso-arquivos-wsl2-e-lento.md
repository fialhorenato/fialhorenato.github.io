---
title: "WSL 2: Acesso a Arquivos e Desempenho no Desenvolvimento"
description: "Veja por que ferramentas Linux podem ficar lentas em arquivos do Windows montados no WSL 2 e como manter os repositórios no sistema de arquivos Linux."
date: 2021-08-28
lang: pt-BR
permalink: /blog/por-que-acesso-arquivos-wsl2-e-lento
translation_url: "/blog/why-wsl2-is-so-slow"
tags:
  - Desenvolvimento de Software
last_modified_at: 2026-11-15
layout: single
locale: pt_BR
translation_label: "Read this article in English"
---

*Read this post in English: [Why WSL 2 File Access Can Slow Down Development](/blog/why-wsl2-is-so-slow).* 

## Resumo

Ao usar ferramentas de desenvolvimento Linux no WSL 2, mantenha os arquivos do projeto no sistema de arquivos Linux. Acessar arquivos através da fronteira entre Windows e Linux pode acrescentar bastante custo de I/O.

## Por que arquivos em uma unidade montada do Windows podem ser lentos

Em 2020, troquei o macOS por um computador com Windows e experimentei o WSL 2 como ambiente de desenvolvimento Linux. No início, mantive os repositórios em uma unidade NTFS montada em `/mnt/d` para também abri-los em aplicativos do Windows.

![Ilustração sobre o desempenho de arquivos no WSL 2](/images/windowsslow.jpg "Desempenho de arquivos no WSL 2")

Conforme os repositórios cresceram, operações de Git e npm pareceram muito mais lentas que na minha configuração anterior. Até `git status` e `git add .` podiam levar vários segundos.

Encontrei então este [artigo de Klee Thomas no Dev.to](https://dev.to/kleeut/why-is-wsl2-so-slow-4n3i), que descrevia uma melhora considerável depois de mover os projetos para fora das partições do Windows montadas.

## A solução: manter projetos Linux no sistema de arquivos Linux

Mova o repositório para o diretório pessoal do WSL e use as ferramentas Linux nessa cópia. Para aplicativos do Windows que precisam dos arquivos, use o sistema de arquivos do Windows. O guia da Microsoft sobre [sistemas de arquivos no WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) explica as diferenças. Este artigo reflete minha configuração de 2021; o desempenho e o suporte das ferramentas continuam evoluindo.
