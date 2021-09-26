---
title: Why WSL2 is very slow?
tags: Windows Technology
style: fill
color: secondary
description: Why WSL2 is usually super slow? Is there a problem in the virtualization?
layout: post
---

## TL;DR

Do not put your data in mounted partitions when using WSL2, use the distro file system and your perfomance will increase significantly.

## Hello!

I maybe forgot to mention here, but after a lot of years being a MacOS user, I changed recently (Ok, it has been almost 1 and 1/2 year) to a Windows desktop. I already had some good reviews from the latest Windows 10 and how could i use WSL/WSL2 for my development setup, then i gave it a shot and a try.

Being very realistic, it fits the purpose of providing a more seamless UNIX experience inside the [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab), and using zsh, you can easily forget that you are really using Windows.

Everything setup, i cloned all my projects and codebases inside a SSD mounted inside my Ubuntu running on the WSL2 on the `/mnt/d`, so then i would be able to use the code inside Windows in a NTFS partition.

![alt text](/images/windowsslow.jpg "Is windows really slow?")

Then, i quickly realized that my `git` commands were becoming very slow as the projects that i was working with grew in size, and my `npm` commands were taking way longer than it used to be in the MacOS.

That frustrated me, since some operations that should usually take seconds to run such as `gst/git status` or even `gaa / git add .` were taking about 5 seconds to complete.

That made me stop by this post on [dev.to](https://dev.to/kleeut/why-is-wsl2-so-slow-4n3i) where Klee Thomas explained that he got a huge perfomance boost by not using the mounted partitions.

So, make yourself a favor and switch to your ~ folder in WSL2 and enjoy those minutes 😉


