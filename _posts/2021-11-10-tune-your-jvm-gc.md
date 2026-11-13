---
title: "JVM Garbage Collection Tuning: G1 GC Tips for Java 8"
tags:
  - Java
  - JVM
  - Performance
  - Garbage collection
description: A historical overview of G1 garbage collection settings and JVM memory tuning for Java 8 services.
last_modified_at: 2026-11-13
layout: single
---

This article collects G1 garbage-collection tuning notes from a Java 8 service. It covers pause-time goals, heap sizing, and a few flags worth understanding.

**Historical note:** JVM defaults and garbage collector behavior vary by JDK version and workload. Treat these as Java 8-era observations, not settings to copy blindly. Measure your application on its target JDK before changing JVM flags.

# G1 garbage collection

## Minor GC vs Major GC vs Full GC

For most backend services that uses micrometer as the metrics framework, you can get JVM GC metrics from it, and if you see the id of the GC occurences, you will see one of those 3 types that i'll try to cover super quickly.

### Minor GC

- Always triggered when JVM is unable to allocate space for a new Object
- Against common belief, all Minor GCs do trigger stop-the-world pauses

### Major GC

- Cleans the Tenured space.


### Full GC

- Cleans the entire Heap – both Young and Tenured spaces.

# Tips

## Set initial and maximum heap sizes deliberately

`-XX:InitialRAMPercentage` and `-XX:MaxRAMPercentage` should be the same.

Setting initial heap size and max heap has advantages. One of them is: you will incur lower Garbage Collection pause times. Because whenever heap size grows from the initial allocated size, it will pause the JVM. It can be circumvented when you set initial, and max heap sizes to be the same. Besides that, if you have under allocated container’s memory size, then JVM will not even start (which is better than experiencing OutOfMemoryError when transactions are in flight).

## Maximum GC Pause

You should consider passing `-XX:MaxGCPauseMillis` argument with your preferred pause time goal. This argument sets a target value for maximum pause time and G1 GC algorithm tries it’s best to reach this goal.

## Avoid setting young gen size

Avoid setting the young generation size to a particular size (by passing `-Xmn, -XX:NewRatio` arguments). 

G1 GC algorithm modifies young generation size at runtime to meet its pause-time goals. If the young generation size is explicitly configured, then pause time goals will not be achieved.

## Remove old arguments

Remove JVM arguments related to old GC algorithms. This won't have effect, or it can even respond in a negative way.

## Consider string deduplication

Eliminate duplicate strings when you pass the `-XX:+UseStringDeduplication` argument. [Here](http://java-performance.info/java-string-deduplication/) is a good explanation about it and [here](https://dzone.com/articles/memory-wasted-by-spring-boot-application) it shows how Spring Boot services memory management can be improved by this.

## Understand the default settings

| Settings                | Description |
|-------------------------|-------------|
| XX:MaxGCPauseMillis=200 | Sets a maximum pause time value. The default value is 200 milliseconds. |
| XX:G1HeapRegionSize=n	 | Sets the size of a G1 region. The value has to be power of two i.e. 256, 512, 1024,…. It can range from 1MB to 32MB.|
| XX:GCTimeRatio=12	     | Sets the total target time that should be spent on GC vs total time to be spent on processing customer transactions. The actual formula for determining the target GC time is [1 / (1 + GCTimeRatio)]. Default value 12 indicates target GC time to be [1 / (1 + 12)] i.e. 7.69%. It means JVM can spend 7.69% of its time in GC activity and remaining 92.3% should be spent in processing customer activity.|
| XX:ParallelGCThreads=n  | Sets the number of the Stop-the-world worker threads. If there are less than or equal to 8 logical processors then sets the value of n to the number of logical processors. Say if your server 5 logical processors then sets n to 5. If there are more than eight logical processors, set the value of n to approximately 5/8 of the logical processors. This works in most cases except for larger SPARC systems where the value of n can be approximately 5/16 of the logical processors.|
| XX:ConcGCThreads=n	 | Sets the number of parallel marking threads. Sets n to approximately 1/4 of the number of parallel garbage collection threads (ParallelGCThreads).|
| XX:InitiatingHeapOccupancyPercent| GC marking cycles are triggered when heap’s usage goes beyond this percentage. The default value is 45%. |
| XX:G1NewSizePercent=5 | Sets the percentage of the heap to use as the minimum for the young generation size. The default value is 5 percent of your Java heap.|
| XX:G1MaxNewSizePercent=60 | Sets the percentage of the heap size to use as the maximum for young generation size. The default value is 60 percent of your Java heap. |
| XX:G1OldCSetRegionThresholdPercent | Sets an upper limit on the number of old regions to be collected during a mixed garbage collection cycle. The default is 10 percent of the Java heap. |
| `-XX:G1ReservePercent` | Sets the percentage of heap capacity to keep available as reserve during evacuation; the default is 10 percent. Check the documentation for the exact JDK you run. |
