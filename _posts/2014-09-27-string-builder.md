---
layout: post
title: Differences between StringBuilder, StringBuffer and String in Java
description: Differences between StringBuilder, StringBuffer and String in Java
modified: 2014-09-27
tags: [StringBuilder, StringBuffer, String, Java]
comments: true
share: true
---

I was reading some articles about the differences between this 3 classes that you can use to build Strings in java and when/how to use.

**StringBuilder** - Is an object that can be changed with low computational cost, it’s cheaper do a .append(“x”) then += “x”.

**Pros** - It’s really cheap to modify and make appends to the String.

**Cons** - Is recommended only if the String will be modified, because is a expensive class than String.

**StringBuffer** - The same as StringBuilder but with synchronized methods, so it can be used with many threads trying to modify the same String.

**Pros** - Assure that the access to the Object is synchronized.

**Cons** - Is the most expensive method to modify Strings, only use if you really need to have synchronized access to the String.

**String** - The most popular Object to build and use Strings, have some good methods.

**Pros** - It’s the cheapest way to create Strings.

**Cons**- Using += to append Strings, or modify the String with this Object is the most expensive way.

**Tips** - Use .concat(“x”) instead of += to append, to modify the String, i recommend to use StringBuilder instead of String.

#### An example of the perfomance of methods adding 1.000 ‘x’s :

StringBuilder = 0.3209839s

String with concat = 1.0130005s

StringBuffer = 1.6049805s

String with += = 1.7210932s

**Source**  - <a href="http://www.examiner.com/article/when-to-use-the-java-string-stringbuffer-and-stringbuilder-classes">When to use the Java String, StringBuffer and StringBuilder classes</a>
