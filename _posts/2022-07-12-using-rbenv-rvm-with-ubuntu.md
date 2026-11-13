---
title: "Installing Ruby with rbenv or RVM on Ubuntu 22.04"
tags:
  - Ruby
  - Ruby
  - Linux
description: Troubleshoot OpenSSL build dependencies when installing Ruby with rbenv or RVM on Ubuntu 22.04.
last_modified_at: 2026-11-13
layout: single
---

As I previously mentioned [here](/blog/why-wsl2-is-so-slow) and [here](/blog/intellij-and-wsl-not-a-good-match), I've been trying to use Windows with Windows Subsystem for Linux (WSL) recently, and unfortunately, failed miserably, it is super slow and unfortunately any Jetbrains IDE and Eclipse have a hard time on scanning the storage for the WSL.

Then, I bought a brand new SSD and installed Ubuntu on its newest version (22.04 currently) and it's been a great ride to come back to Linux as a development platform (It is a way better experience).

Well, as you probably know, this blog uses [jekyll](https://jekyllrb.com/) under the hood, and jekyll is built on top of Ruby, making it necessary for me to have Ruby installed in my computer, and to try to break things in a controlled way, I always tend to install virtual environments that can be "easily" destroyed.

For Ruby version management, I have used [RVM](https://rvm.io/) and [rbenv](https://github.com/rbenv/rbenv). In 2022, an older Ruby build on Ubuntu 22.04 led me to install an archived OpenSSL 1.1 package manually.

That archived-package workaround is removed here: it pins an obsolete system library and should not be treated as current installation advice. Ruby build prerequisites vary by Ruby and Ubuntu version. Update `ruby-build` and follow its [current troubleshooting guidance](https://github.com/rbenv/ruby-build/wiki); for an OpenSSL build error, install supported development headers for your distribution rather than downloading an old `.deb` from an archive.

The main lesson from this setup was to check the Ruby version’s OpenSSL compatibility and the version manager’s build instructions before compiling. This article records my Ubuntu 22.04 experience from 2022, not a current installation recipe.

Any questions, just [send me a message](/contact).
