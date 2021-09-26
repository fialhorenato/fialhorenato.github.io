---
title: Starting with Flutter - Part 1
tags: Flutter Technology
style: fill
color: primary
description: Learning from start working with Flutter in Windows
layout: post
---

Hello!

I've been challenging myself to learn new languages/technologies during since last year, but ~~laziness~~ because of work, it was hard to find time, 
but then i ~~stopped being lazy~~ found some time to learn a framework and language that i've been postponing since last year, ~~Go and Protobuf~~ **Flutter and Dart**!

I'll try to bring here how was my learning process, biggest difficulties (Since i'm doing this in a Windows Desktop) and how to work them out.

## Installing

I never thought that i would say this after 10+ years in the software development, but installing Flutter on Windows is hard, there are a lot of its and bits and
even using Android Studio, i faced some issues.

### First things first, download

You'll need to download the latest Flutter SDK from the [webpage](https://flutter.dev/docs/get-started/install), i'll deep dive more in the Windows setup since is the one
I have more recent experience with and it is for sure the most complex.

### Android Studio with Flutter

Well, flutter supports a lot of IDEs such as Visual Studio Code, IntelliJ, Eclipse, but the main one that everyone loves is the ~~in~~famous Android Studio, that you can
download for free [here](https://developer.android.com/studio/) or if you already use other IntelliJ products, i suggest you to download the [Jetbrains Toolbox](https://www.jetbrains.com/toolbox-app/) and download it from there.

### Configuring

Even though i mostly use Flutter in WSL2, unfortunately it doesn't work very well with Flutter, there is a [tutorial](https://stackoverflow.com/questions/62857688/how-to-make-flutter-work-on-wsl2-using-hosts-emulator) on Stackoverflow on how to install and use WSL2, i wanted to have a better experience, but if you want to adventure yourself, go ahead!

In this post i'll focus here most on using in the ~~in~~famous Powershell.

Assuming that you won't add Flutter to your PATH on Windows, lets agree that <FLUTTER_PATH> is the path of your Flutter.bat file (Eg: `D:\Frameworks\Flutter\flutter-2.5.0\flutter\bin\Flutter.bat`).


Then you need to run `<FLUTTER_PATH> doctor` to understand what you need to do in order to configure your environment! 

The output should be something like this:

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

First things first, you must run `<FLUTTER_PATH> config --android-studio-dir="<PATH_TO_YOUR_ANDROID_STUDIO"` (Eg: `flutter config --android-studio-dir="C:\Program Files\Android\Android Studio"`)

That will let Flutter Know which Android Studio you want to use with it!

### Android Studio

After telling flutter with Android Studio are you using, open the ~~in~~famous IDE, as i'm writing this post, the version used is `2020.3.1`, i'll promise to try to update this post (or the following ones) if something breaks/changes, but that is the most recent version I have.

After opening Android Studio, go to `File > Settings > Plugins > Marketplace` and search for `Flutter`, it is the first [result](https://plugins.jetbrains.com/plugin/9212-flutter)

This is the official plugin from the Flutter team and it is essential to work with Flutter on Android Studio.

Then, after downloading and restarting your Android Studio, create a new Flutter Project!

You will be presented with a Screen to pinpoint your Flutter SDK path, point it to the root of your Flutter folder , for example `D:\Frameworks\flutter_windows_2.5.0-stable\flutter`

Then, select your Project Name, Location and everything, and wait for Android Studio to do its magic and bring the project to you.



### Default Project

When you create a Flutter Project on Android Studio, it already brings you an example of project for you to Run against the emulators you have or to rely on some code to start your life with Flutter. Use it with wisdom, since it is only an example and it doesn't provide you a good architecture/organization of a big project.



### Moving forward

I'll end this part from here, in the next post i'll focus more on the inner bits of Flutter and Dart (Which has a syntax very close to Java).

But if you don't want to wait and have a need to keep moving forward, i suggest you to check the `examples` folder inside the Flutter SDK and/or the famous [Startup name generator](https://flutter.dev/docs/get-started/codelab) tutorial that the flutter team gives to you.

The [documentation](https://flutter.dev/docs/get-started/editor) is a good start point as well!


My first app is about to be released in the Google Play store and i'm super excited about it!

