---
title: "Como Configurar o Flutter no Windows com Android Studio"
description: "Tutorial histórico do Flutter 2.5 sobre SDK no Windows, plugin do Android Studio, flutter doctor e onde encontrar instruções atuais."
date: 2021-09-10
lang: pt
permalink: /blog/configurar-flutter-windows-android-studio
translation_url: /blog/starting-with-flutter
tags:
  - Desenvolvimento de Software
last_modified_at: 2026-11-15
layout: single
---

*Read this post in English: [Set Up Flutter on Windows with Android Studio](/blog/starting-with-flutter).* 

Este artigo registra como configurei o Flutter 2.5 e o Android Studio no Windows em 2021. É um passo a passo histórico, não um guia de instalação atual; consulte o [guia oficial de instalação do Flutter](https://docs.flutter.dev/get-started/install) para comandos e pré-requisitos atualizados.

## Preparar o ambiente de desenvolvimento

Uma configuração funcional do Flutter precisa do SDK, de um editor ou IDE e das ferramentas de plataforma para os destinos desejados. Em 2021, usei o Android Studio no Windows; os passos abaixo mantêm esse contexto.

### 1. Instalar o SDK do Flutter

Baixe o SDK do Flutter seguindo o [guia oficial de instalação](https://docs.flutter.dev/get-started/install). Este exemplo histórico foca no Windows, sistema que eu conhecia melhor na época.

### 2. Escolher um editor ou IDE

O Flutter aceita diversos editores e IDEs, incluindo Visual Studio Code e IDEs baseadas em IntelliJ. Este passo a passo usa o Android Studio, que pode ser baixado no [site do Android Studio](https://developer.android.com/studio/). Quem já usa produtos JetBrains também pode gerenciar instalações pela [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/).

### 3. Conferir as ferramentas

Na época, achei o Flutter no WSL 2 menos direto que uma configuração nativa no Windows. O suporte e os fluxos podem ter mudado; consulte a documentação atual do Flutter e da Microsoft se quiser usar WSL.

Os comandos abaixo usam PowerShell e refletem a configuração Windows que utilizei em 2021.

Se o Flutter não estiver no `PATH`, defina `<FLUTTER_PATH>` como o caminho de `flutter.bat`, por exemplo `D:\Frameworks\Flutter\flutter-2.5.0\flutter\bin\flutter.bat`.

Execute o diagnóstico e use a saída para identificar componentes ausentes:

```powershell
<FLUTTER_PATH> doctor
```

Em 2021, uma instalação Flutter 2.5 poderia exibir resultados parecidos com estes:

```
[√] Flutter (Channel stable, 2.5.0, on Microsoft Windows [Version 10.0.19042.1165], locale en-US)
[X] Android toolchain - develop for Android devices (Android SDK version 31.0.0)
[√] Chrome - develop for the web
[X] Android Studio (version 2020.3)
[X] Android Studio
[X] IntelliJ IDEA Ultimate Edition (version 2021.2)
[√] VS Code (version 1.59.1)
[X] Connected device
```

Se o Flutter não detectasse o Android Studio automaticamente, a CLI de 2021 oferecia esta configuração (substitua pelo caminho da sua instalação):

```powershell
<FLUTTER_PATH> config --android-studio-dir="C:\Program Files\Android\Android Studio"
```

Isso informa à ferramenta de linha de comando do Flutter onde está a instalação do Android Studio. Talvez essa opção não seja necessária se o Flutter detectar a IDE automaticamente.

### 4. Configurar o Android Studio

Depois de configurar o caminho da IDE, abra o Android Studio. As capturas de tela e versões citadas neste artigo são de 2021; os nomes dos menus podem ter mudado.

No Android Studio, abra o gerenciador de plugins, procure o plugin oficial do [Flutter](https://plugins.jetbrains.com/plugin/9212-flutter) e instale-o. Os rótulos da interface podem variar conforme a versão do Android Studio.

Reinicie a IDE, se solicitado, crie um projeto Flutter e selecione o diretório do SDK quando isso for pedido. Na minha instalação de 2021, o caminho era `D:\Frameworks\flutter_windows_2.5.0-stable\flutter`.

## Criar e executar um projeto inicial

Um novo projeto Flutter inclui um aplicativo de exemplo simples, que pode ser executado em um emulador ou dispositivo conectado. Use-o como estrutura inicial de aprendizado; uma aplicação de produção precisa de uma arquitetura e organização adequadas aos requisitos.

## Continuar aprendendo

Esta configuração é só o começo. Consulte os recursos atuais de aprendizado do Flutter para explorar Dart e desenvolver uma aplicação completa.

Para instruções atualizadas e projetos, comece pela [documentação do Flutter](https://docs.flutter.dev/) e pelos materiais de aprendizado.

Quando escrevi as anotações originais, estava animado para preparar meu primeiro aplicativo para o Google Play. Hoje, este artigo também registra esse marco de aprendizado, não apenas um processo de configuração.
