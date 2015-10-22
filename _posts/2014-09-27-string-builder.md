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

### StringBuilder

Is an object that can be changed with low computational cost, it’s cheaper do a ```string.append(“x”)``` than ``string += “x”.``

**Pros** - It’s really cheap to modify and make appends to the String.

**Cons** - Is recommended only if the String will be modified, because is a expensive class than String.

###StringBuffer

The same as StringBuilder but built with synchronized methods, so it guarantees the synchronization with many threads trying to modify the same String.

**Pros** - Assure that the access to the Object is synchronized.

**Cons** - Is the most expensive method to modify Strings, only use if you really need to have synchronized access to the String.

###String

The most popular Object to build and use Strings, have some good methods.

**Pros** - It’s the cheapest way to create Strings.

**Cons**- Using += to append Strings, or modify the String with this Object is the most expensive way.

###Conclusions

**Tips** - Use ``string.concat(“x”)`` instead of ``string += "x"`` to append, to modify the String.

I recommend to use StringBuilder instead of String.

#### An example of the perfomance of methods adding 1.000 "x" :

StringBuilder using .append("x") = 0.3209839s

String with concat("x") = 1.0130005s

StringBuffer = 1.6049805s

String with += = 1.7210932s

**Source**  - <a href="http://www.examiner.com/article/when-to-use-the-java-string-stringbuffer-and-stringbuilder-classes">When to use the Java String, StringBuffer and StringBuilder classes</a>
