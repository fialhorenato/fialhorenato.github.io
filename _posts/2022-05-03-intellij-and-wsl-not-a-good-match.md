---
title: "Run IntelliJ IDEA with a WSL Development Environment"
tags:
  - Software Development
description: "A first-hand account of configuring IntelliJ IDEA, WSLg, and Gradle, with links to current JetBrains guidance."
last_modified_at: 2026-11-13
layout: single
---

This is a 2022 account of running IntelliJ IDEA inside WSLg after I had trouble importing a Gradle project through my Windows IDE setup. WSL and JetBrains support have changed since then, so check the current [JetBrains WSL development documentation](https://www.jetbrains.com/help/idea/how-to-use-wsl-development-environment-in-product.html) before following these steps.

This post follows my earlier notes on [WSL 2 file performance](/blog/why-wsl2-is-so-slow).

I had used macOS as my main development environment since 2014. In 2020, I built a Windows desktop for gaming and started looking for a Linux-like development workflow without dual-booting.

I had disliked maintaining a Windows/Ubuntu dual-boot setup, but I still wanted familiar terminal tools such as `sdkman`. A friend introduced me to Windows Subsystem for Linux (WSL), which made it possible to use an Ubuntu environment from Windows.

At the time, I ran into slow Gradle imports when IntelliJ on Windows worked with project files and Gradle inside WSL. Keeping the IDE and project tools in one environment was the workaround I chose; it was a personal experience, not a claim about current JetBrains support.

When IntelliJ IDEA 2022.1 came out, I tried it with Kotlin projects built by Gradle inside WSL. In my setup, indexing and project import became very slow—sometimes taking hours. This was a report from one combination of IDE, Gradle, Windows, and WSL, not a general performance benchmark.

I suspected file scanning contributed to the delay, but disabling security software was not an acceptable solution for me.

## Why Gradle imports were slow

I switched to running JetBrains Toolbox and IntelliJ inside WSLg, keeping the IDE, project files, and Gradle in the same environment. WSLg enables Linux GUI applications on supported Windows installations. Current JetBrains WSL workflows may differ; consult the linked current documentation before choosing an approach.

## The workaround: run the IDE in WSLg

### 1. Update WSL

The commands below reflect my Windows 11 setup in 2022. Check current Microsoft guidance for supported Windows and WSL versions. To update WSL, run this in PowerShell:

```bash
wsl --update
```

After the update, restart the WSL virtual machine with:

```powershell
wsl --shutdown
```

### 2. Confirm Linux GUI support

On a WSLg-enabled installation, you can confirm Linux GUI support by installing a small desktop application such as Nautilus:

```bash
sudo apt install nautilus -y
```

Launch it from the WSL terminal:

![Nautilus file manager running as a Linux GUI application in WSLg](/images/nautiluswslg.png "Nautilus running on WSLg")

### 3. Install JetBrains Toolbox

I use [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) to install and manage JetBrains IDEs.

Download the Linux archive from the Toolbox website, either in WSL or through Windows, and place it in the WSL filesystem.

Extract the archive in your home directory (the filename will vary by version):

```bash
sudo tar -xzf jetbrains-toolbox-1.23.11849.tar.gz -C ~/
```

Then launch Toolbox from the extracted directory. On my system, the desktop launcher appeared in the applications menu:

![JetBrains Toolbox running inside the WSLg environment](/images/toolboxwslg.png "Toolbox running on WSLg")

### Troubleshoot the application shortcut

On my system, Toolbox created a desktop entry under `~/.local/share/applications`. If the app shortcut is missing, inspect the generated entry and follow the current desktop-environment guidance before copying files into a system directory.

```bash
ls ~/.local/share/applications
```

Check whether Toolbox created a `.desktop` entry and follow your desktop environment’s current guidance to refresh or register the launcher. Avoid copying every desktop file into a system directory without checking its contents and permissions.

## Takeaway

Running the IDE, project files, and build tools in the same environment resolved the import delay in my setup. WSL and JetBrains have changed substantially since 2022, so compare this historical workaround with the current [JetBrains WSL development guide](https://www.jetbrains.com/help/idea/how-to-use-wsl-development-environment-in-product.html) before adopting it.

