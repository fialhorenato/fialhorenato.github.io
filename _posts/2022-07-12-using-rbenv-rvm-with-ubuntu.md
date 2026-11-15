---
title: "Install Ruby with rbenv or RVM on Ubuntu 22.04"
tags:
  - Software Development
description: "Notes from building Ruby with rbenv or RVM on Ubuntu 22.04, including OpenSSL compatibility and links to current troubleshooting guidance."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
header:
  image: /images/post-covers/using-rbenv-rvm-with-ubuntu.svg
  image_description: "Install Ruby with rbenv or RVM on Ubuntu 22.04"
---

After experimenting with [WSL 2 file access](/blog/why-wsl2-is-so-slow) and [IntelliJ inside WSLg](/blog/intellij-and-wsl-not-a-good-match), I installed Ubuntu directly on a separate SSD for my development environment. This is a personal account of that 2022 setup, not a comparison of current WSL and Linux performance.

This blog is built with [Jekyll](https://jekyllrb.com/), which requires Ruby. I use a Ruby version manager so the project can use its required Ruby version without replacing the system Ruby.

For Ruby version management, I have used [RVM](https://rvm.io/) and [rbenv](https://github.com/rbenv/rbenv). In 2022, building an older Ruby release on Ubuntu 22.04 exposed an OpenSSL compatibility issue.

That archived-package workaround is removed here: it pins an obsolete system library and should not be treated as current installation advice. Ruby build prerequisites vary by Ruby and Ubuntu version. Update `ruby-build` and follow its [current troubleshooting guidance](https://github.com/rbenv/ruby-build/wiki); for an OpenSSL build error, install supported development headers for your distribution rather than downloading an old `.deb` from an archive.

The main lesson from this setup was to check the Ruby version’s OpenSSL compatibility and the version manager’s build instructions before compiling. This article records my Ubuntu 22.04 experience from 2022, not a current installation recipe.

Choose a Ruby version manager, install the project’s required Ruby version, and use the current build instructions for that Ruby and Ubuntu release. If you run into a build problem, consult the version manager’s troubleshooting guidance before changing system libraries. Questions or corrections are welcome via the [contact page](/contact).
