---
title: "Set Up Flutter on Windows with Android Studio"
tags:
  - Software Development
description: "A historical Flutter 2.5 walkthrough covering the Windows SDK setup, Android Studio plugin, flutter doctor, and where to find current instructions."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
translation_url: "/blog/configurar-flutter-windows-android-studio"
translation_label: "Leia este artigo em português"
---

This post records how I set up Flutter 2.5 and Android Studio on Windows in 2021. It is a historical walkthrough, not a current installation recipe; use the official [Flutter installation guide](https://docs.flutter.dev/get-started/install) for up-to-date commands and prerequisites.

## Set up the development environment

A working Flutter setup needs the SDK, an editor or IDE, and the platform tools for the targets you want to build. In 2021, I used Android Studio on Windows; the steps below preserve that context.

### 1. Install the Flutter SDK

Download the Flutter SDK using the official [Flutter installation guide](https://docs.flutter.dev/get-started/install). In this historical example, I focus on Windows because it was the setup I knew best at the time.

### 2. Choose an editor or IDE

Flutter supports several editors and IDEs, including Visual Studio Code and IntelliJ-based IDEs. This walkthrough uses Android Studio, which you can download from the [Android Studio website](https://developer.android.com/studio/). If you already use JetBrains products, [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) is another way to manage IDE installations.

### 3. Check the toolchain

At the time, I found Flutter on WSL 2 less straightforward than a native Windows setup. Support and workflows may have changed, so consult the current Flutter and Microsoft documentation if you want to use WSL.

The commands below use PowerShell and reflect the Windows setup I used in 2021.

If Flutter is not on your `PATH`, set `<FLUTTER_PATH>` to the location of `flutter.bat`, for example `D:\Frameworks\Flutter\flutter-2.5.0\flutter\bin\flutter.bat`.

Run the diagnostic command and use its output to identify missing components:

```powershell
<FLUTTER_PATH> doctor
```

A Flutter 2.5 installation in 2021 could report results like these:

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

If Flutter did not detect Android Studio automatically, the 2021 CLI offered this setting (replace the path with your installation):

```powershell
<FLUTTER_PATH> config --android-studio-dir="C:\Program Files\Android\Android Studio"
```

This tells the Flutter command-line tool which Android Studio installation to use. You may not need this option if Flutter detects the IDE automatically.

### 4. Configure Android Studio

After configuring the IDE path, open Android Studio. The screenshots and version references in this article are from 2021, so menu names may differ in current releases.

In Android Studio, open the plugin manager, search for the official [Flutter plugin](https://plugins.jetbrains.com/plugin/9212-flutter), and install it. UI labels can differ across Android Studio releases.

Restart the IDE if requested, create a Flutter project, and select the Flutter SDK directory when prompted. For my 2021 installation, it looked like `D:\Frameworks\flutter_windows_2.5.0-stable\flutter`.


## Create and run a starter project

A new Flutter project includes a small sample application you can run on an emulator or connected device. Treat it as a learning scaffold; a production app needs an architecture and organization suited to its requirements.


## Continue learning

This setup is only the starting point; continue with the current Flutter learning resources to explore Dart and build a complete application.

For current setup instructions and projects, start with the [Flutter documentation](https://docs.flutter.dev/) and its learning resources.

When I wrote the original notes, I was excited to be preparing my first app for Google Play. Looking back, this post is a record of that learning milestone as much as it is a setup guide.

