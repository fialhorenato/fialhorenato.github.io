---
title: "Java Virtual Threads: From the Java 19 Preview to Java 21"
tags:
  - Software Development
description: "An updated overview of Java virtual threads, including how the Java 19 preview example differs from the finalized Java 21 API."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
header:
  image: /images/post-covers/working-with-new-virtual-threads-java-19.svg
  image_description: "Java Virtual Threads: From the Java 19 Preview to Java 21"
---

## What are virtual threads?

[Java 19](https://jdk.java.net/19/release-notes) introduced virtual threads as a preview feature. They are lightweight threads designed to make high-throughput concurrent applications easier to write and maintain. This article captures an early preview; virtual threads became a permanent feature in Java 21. See Oracle’s [Java 19 preview notes](https://docs.oracle.com/en/java/javase/19/core/virtual-threads.html) and [Java 21 migration guide](https://docs.oracle.com/en/java/javase/21/migrate/significant-changes-jdk-release.html) for the version history.

Virtual threads are part of Project Loom and let applications use the familiar `Thread` API with many lightweight threads. They can help workloads that spend substantial time waiting on I/O; they do not make CPU-bound work faster or remove the need to manage downstream concurrency. Platform threads remain available for work that needs them.

## Create a virtual thread (Java 19 preview example)

In Java 19, this API was in preview, so compiling and running the example required the `--enable-preview` flag. That requirement applies to this Java 19 example, not to the final API in Java 21 and later.

If you are an IntelliJ user, you can tell IntelliJ to use this flag by going into the `Open Module Settings -> Project -> Language Level` and choose the `Java 19 (Preview)`.

```java
    // Declare a runnable that will print the information about the current thread
    Runnable printThread = () -> System.out.println(Thread.currentThread());

    // Declare a virtual thread
    var virtualThread = Thread.ofVirtual()
        .start(printThread);

    // Declare a platform thread
    var platformThread = Thread.ofPlatform()
        .start(printThread);
```

The output will be:

```java
    VirtualThread[#22]/runnable@ForkJoinPool-1-worker-1
    Thread[#24,Thread-0,5,main]
```

The output shows the virtual thread mounted on a carrier worker and a separate platform thread. Runtime output varies by JDK and execution timing.

## Coordinate virtual and platform threads

Virtual threads support ordinary Java synchronization. In early JDK releases, blocking while holding a monitor could pin a carrier thread; consult the JDK-version-specific guidance when diagnosing pinning. The example below demonstrates coordination, not a general performance recommendation.

```java
class VirtualThreads {

    public static void main(String[] args) {
        var c = new VirtualThreads();
        c.start();
    }

    public void start() {
        var virtualThread = Thread.ofVirtual();
        var platformThread = Thread.ofPlatform();

        virtualThread.start(() -> {
            System.out.println(Thread.currentThread() + " running command A");
            synchronized(this) {
                try {
                    this.wait();
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
            System.out.println(Thread.currentThread() + " running command C");
        });

        platformThread.start(() -> {
            System.out.println(Thread.currentThread() + " running command B");
            synchronized(this) {
                this.notifyAll();
            }
        });
    }
}
``` 

The output will be:

```java
    VirtualThread[#22]/runnable@ForkJoinPool-1-worker-1 running command A
    Thread[#24,Thread-0,5,main] running command B
    VirtualThread[#22]/runnable@ForkJoinPool-1-worker-1 running command C
```

Loom and Java in general are prominently devoted to building web applications. Obviously, Java is used in many other areas, and the ideas introduced by Loom may well be useful in these applications. 

It’s easy to see how massively increasing thread efficiency, and dramatically reducing the resource requirements for handling multiple competing needs, will result in greater throughput for servers. Better handling of requests and responses is a bottom-line win for a whole universe of existing and to-be-built Java applications.


## Reference

- [Project Loom](https://jdk.java.net/loom/)
- [Infoworld](https://www.infoworld.com/article/3652596/project-loom-understand-the-new-java-concurrency-model.html)


