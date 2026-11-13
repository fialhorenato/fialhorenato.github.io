---
title: "Why WSL 2 File Access Can Slow Down Development"
tags:
  - WSL 2
  - Windows
  - Developer tools
description: Learn why Linux tools in WSL 2 can slow down on a mounted Windows drive and where to keep your project files.
last_modified_at: 2026-11-13
layout: single
---

## TL;DR

When you run Linux development tools in WSL 2, keep your project files in the Linux filesystem. Accessing files across the Windows/Linux boundary can add significant I/O overhead.

## Why files on a mounted Windows drive can feel slow

In 2020, I moved from macOS to a Windows desktop and tried WSL 2 as my Linux development environment. The terminal experience was familiar, but I initially stored repositories on a Windows-mounted drive and ran Linux tools against them.

Being very realistic, it fits the purpose of providing a more seamless UNIX experience inside the [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab), and using zsh, you can easily forget that you are really using Windows.

Everything setup, i cloned all my projects and codebases inside a SSD mounted inside my Ubuntu running on the WSL2 on the `/mnt/d`, so then i would be able to use the code inside Windows in a NTFS partition.

![alt text](/images/windowsslow.jpg "Is windows really slow?")

Then, i quickly realized that my `git` commands were becoming very slow as the projects that i was working with grew in size, and my `npm` commands were taking way longer than it used to be in the MacOS.

That frustrated me, since some operations that should usually take seconds to run such as `gst/git status` or even `gaa / git add .` were taking about 5 seconds to complete.

That led me to this [Dev.to post by Klee Thomas](https://dev.to/kleeut/why-is-wsl2-so-slow-4n3i), which described a substantial performance improvement after moving projects off mounted Windows partitions.

Move the repository into your WSL home directory and run Linux tools against that copy. For Windows applications that need the files, use the Windows filesystem instead. Microsoft’s [WSL filesystem guidance](https://learn.microsoft.com/en-us/windows/wsl/filesystems) explains the trade-offs. This post reflects my 2021 setup; performance and tooling support continue to evolve.


