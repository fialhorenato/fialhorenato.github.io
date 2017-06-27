---
layout: post
title: How to deal with money currency using java
description: How to deal with money currency using java
modified: 2017-04-05
tags: [Money, Java, Double, BigDecimal]
comments: true
share: true
---

As is widespread and known that Java is a typo language and the language primitives typos are not very good to deal with money currency because.

I got a job interview for a Java Developer Analyst that gave me a test of developing a system that calculate the best change for an specific amount, and that's when i realize how double or float or even BigDecimal are the nightmare if you want to work with currency.

Getting home and reading more about how we should treat currency in Java i heard a lot about some projects, one of them that is amazing is [JavaMoney](http://javamoney.github.io/), that you should take a look if you need to work with money currency.

In my case, since i was doing the test using paper and no internet at all, went directly to use double.

I did this and worked for me, if you want to get a specific double and treat it using 2 decimals only, it's amazing!

{% gist fialhorenato/67e28e214c0236b33013cdf33bfed1d2 %}

```java
String formatted = String.format("%.2f", double yourdoublewithNdecimals);
double newdoublewith2decimal = Double.parseDouble(formatted));
```

The only thing that you can't forget is that if you make any operation with this double, will generate doubles with more than 2 decimals, so everytime you need to treat this "error".

If you wanna check the code for the interview is [here](https://gist.github.com/fialhorenato/ef6e159ba5a37df01424875d2722d5f7)
