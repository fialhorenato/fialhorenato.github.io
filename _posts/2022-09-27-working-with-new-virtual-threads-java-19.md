---
title: Working with virtual threads on Java 19
tags: Java Development
style: fill
color: secondary
description: How to use the new virtual threads on Java 19
layout: post
---

## What?

[Java 19](https://jdk.java.net/19/release-notes) is coming, and with this new version of Java, it brings an amazing new feature, virtual threads.

This update comes to reduce the effort of writing, maintaining, and observing high-throughput, concurrent applications.

This is part of the [Project Loom](https://www.infoworld.com/article/3652596/project-loom-understand-the-new-java-concurrency-model.html), a project that aims to bring a new concurrency model to java, but preserving the same simple abstraction to the developers.

Don't worry, you will still be able to use the platform threads.

## How?

Currently, those implementations are on preview mode, so you must provide the `--enable-preview` flag to the JVM.

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


## Reference

- [Project Loom](https://jdk.java.net/loom/)
- [Infoworld](https://www.infoworld.com/article/3652596/project-loom-understand-the-new-java-concurrency-model.html)


