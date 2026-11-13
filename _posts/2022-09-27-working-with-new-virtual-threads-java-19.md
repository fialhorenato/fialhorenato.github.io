---
title: "Java 19 Virtual Threads: An Early Look at Project Loom"
tags:
  - Java
  - Virtual threads
  - Concurrency
description: An early look at Java 19 preview virtual threads, platform threads, and Project Loom.
last_modified_at: 2026-11-13
layout: single
---

## What are virtual threads?

[Java 19](https://jdk.java.net/19/release-notes) introduced virtual threads as a preview feature. They are lightweight threads designed to make high-throughput concurrent applications easier to write and maintain. This article captures an early preview; virtual threads became a permanent feature in Java 21. See Oracle’s [Java 19 preview notes](https://docs.oracle.com/en/java/javase/19/core/virtual-threads.html) and [Java 21 migration guide](https://docs.oracle.com/en/java/javase/21/migrate/significant-changes-jdk-release.html) for the version history.

This update comes to reduce the effort of writing, maintaining, and observing high-throughput, concurrent applications.

This is part of the [Project Loom](https://www.infoworld.com/article/3652596/project-loom-understand-the-new-java-concurrency-model.html), a project that aims to bring a new concurrency model to java, but preserving the same simple abstraction to the developers.

Don't worry, you will still be able to use the platform threads.

## How?

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

Now you see that we have a virtual thread executing on a worker thread of the Fork-Join pool, and another platform thread running on the main process.

## Seamless integration between platform and virtual threads

Synchronized blocks will work transparent in between virtual and platform threads, as it is shown in this example.

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


