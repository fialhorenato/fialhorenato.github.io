---
title: How to use rbenv or rvm with Ubuntu 22.04
tags: Ruby Ubuntu Linux
style: fill
color: light
description: Quick reminder of problems by using rbenv or rvm in Ubuntu 22.04
layout: post
---

As I previously mentioned [here](/blog/why-wsl2-is-so-slow) and [here](/blog/intellij-and-wsl-not-a-good-match), I've been trying to use Windows with Windows Subsystem for Linux (WSL) recently, and unfortunately, failed miserably, it is super slow and unfortunately any Jetbrains IDE and Eclipse have a hard time on scanning the storage for the WSL.

Then, I bought a brand new SSD and installed Ubuntu on its newest version (22.04 currently) and it's been a great ride to come back to Linux as a development platform (It is a way better experience).

Well, as you probably know, this blog uses [jekyll](https://jekyllrb.com/) under the hood, and jekyll is built on top of Ruby, making it necessary for me to have Ruby installed in my computer, and to try to break things in a controlled way, I always tend to install virtual environments that can be "easily" destroyed.

For ruby, I always used [rvm](https://rvm.io/) or [rbenv](https://github.com/rbenv/rbenv), and both of them gave me some "hard" time installing in the newest Ubuntu 22.04 due to the deprecation of OpenSSL 1.0.

I'll update this post later in the future, but this is the trick you need to make it happen:

```shell
wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1l-1ubuntu1.6_amd64.deb 
&& 
sudo dpkg -i libssl1.1_1.1.1l-1ubuntu1.6_amd64.deb
```

This command will download the LibSSL 1.1 for ubuntu and install it using the package manager `dpkg`, that should fix the issue!

Any questions, just [send me a message](/contact).