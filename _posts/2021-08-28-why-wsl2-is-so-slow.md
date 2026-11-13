---
title: "Why WSL 2 File Access Can Slow Down Development"
tags:
  - Software Development
description: "Learn why Linux tools may run slowly on Windows-mounted files in WSL 2 and how keeping repositories in the Linux filesystem can help."
last_modified_at: 2026-11-13
layout: single
---

## TL;DR

When you run Linux development tools in WSL 2, keep your project files in the Linux filesystem. Accessing files across the Windows/Linux boundary can add significant I/O overhead.

## Why files on a mounted Windows drive can feel slow

In 2020, I moved from macOS to a Windows desktop and tried WSL 2 as my Linux development environment. I initially kept repositories on an NTFS drive mounted under `/mnt/d` so I could also open them from Windows applications.

![Illustration accompanying the discussion of WSL 2 file performance](/images/windowsslow.jpg "WSL 2 file performance")

As the repositories grew, Git and npm operations felt much slower than they had on my previous setup. Even `git status` and `git add .` could take several seconds.

That led me to this [Dev.to post by Klee Thomas](https://dev.to/kleeut/why-is-wsl2-so-slow-4n3i), which described a substantial performance improvement after moving projects off mounted Windows partitions.

## The fix: keep Linux projects in the Linux filesystem

Move the repository into your WSL home directory and run Linux tools against that copy. For Windows applications that need the files, use the Windows filesystem instead. Microsoft’s [WSL filesystem guidance](https://learn.microsoft.com/en-us/windows/wsl/filesystems) explains the trade-offs. This post reflects my 2021 setup; performance and tooling support continue to evolve.


