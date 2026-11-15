---
title: "Java 8 G1 Garbage Collection: Tuning Notes and Trade-Offs"
tags:
  - Software Development
description: "Review Java 8 G1 garbage collection concepts, heap and pause-time settings, and why JVM flags should be measured on your own workload."
last_modified_at: 2026-11-13
layout: single
lang: en
locale: en_US
translation_url: "/blog/ajustar-g1-garbage-collector-java-8"
translation_label: "Leia este artigo em português"
---

This article collects G1 garbage-collection tuning notes from a Java 8 service. It covers pause-time goals, heap sizing, and a few flags worth understanding.

**Historical note:** JVM defaults and garbage collector behavior vary by JDK version and workload. Treat these as Java 8-era observations, not settings to copy blindly. Measure your application on its target JDK before changing JVM flags.

## G1 garbage collection

## Minor GC vs Major GC vs Full GC

Micrometer can expose garbage-collection metrics for JVM services. The exact event names and collector behavior depend on the JDK and collector; the brief terminology below reflects older HotSpot and Java 8 discussions.

### Minor GC

- Typically reclaims young-generation regions.
- G1 collection pauses are stop-the-world, although concurrent marking work can occur alongside application threads.

### Major GC

- “Major GC” is often used informally for collection work involving old-generation memory, but it is not a universally precise G1 event label.


### Full GC

- A full GC reclaims the heap and is generally a high-impact event; investigate its cause rather than assuming it is routine.

## Heap and pause-time tuning

### Set initial and maximum heap sizes deliberately

Choosing initial and maximum heap sizes is a workload and container-sizing decision. Matching `-XX:InitialRAMPercentage` and `-XX:MaxRAMPercentage` can avoid later heap expansion, but it also reserves more memory up front and leaves less room for native memory and other processes. Measure startup, memory use, and pauses under realistic load before pinning the values.

### Set a pause-time goal

`-XX:MaxGCPauseMillis` sets a pause-time goal, not a hard upper bound. G1 uses it as one input when choosing collection work; a more aggressive goal can affect throughput and does not guarantee every pause stays below the target.

### Let G1 size the young generation

Avoid setting the young generation size to a particular size (by passing `-Xmn, -XX:NewRatio` arguments). 

G1 adjusts the young generation based on its pause-time goals. Fixed young-generation settings can restrict that adaptation, so avoid tuning them without measurements and a specific reason.

### Remove obsolete collector flags

Remove flags for collectors you no longer use. Some options may be ignored or conflict with the selected collector; check the target JDK’s unified logging and option documentation.

### Consider string deduplication

On supported G1 configurations, `-XX:+UseStringDeduplication` can reduce memory used by duplicate strings, at the cost of additional work. Profile the application first and consult the documentation for the target JDK before enabling it.

## JVM options to recognize

| JVM option | What it controls | Practical note |
| --- | --- | --- |
| `-XX:MaxGCPauseMillis` | A pause-time goal for G1 | A target, not a hard guarantee; the default depends on JDK version. |
| `-XX:G1HeapRegionSize` | Region size in the G1 heap | Usually ergonomically selected. Set only after measurement. |
| `-XX:GCTimeRatio` | Desired ratio between GC time and application time | A tuning input, not a promise of a fixed percentage. |
| `-XX:ParallelGCThreads` | Worker threads for stop-the-world phases | Defaults are based on available processors and can be container-aware. |
| `-XX:ConcGCThreads` | Workers for concurrent marking | Defaults vary; changing it trades CPU availability against GC progress. |
| `-XX:InitiatingHeapOccupancyPercent` | Occupancy threshold that can start concurrent marking | Adaptive IHOP can adjust behavior; check the target JDK’s documentation. |
| `-XX:G1NewSizePercent`, `-XX:G1MaxNewSizePercent` | Bounds for the young generation size | Avoid pinning these without evidence; G1 adjusts young size to meet goals. |
| `-XX:G1OldCSetRegionThresholdPercent` | Limit on old regions selected in a mixed collection | Verify availability and semantics for the exact JDK release. |
| `-XX:G1ReservePercent` | Heap capacity reserved to reduce evacuation failure risk | Increasing it reduces usable application heap; default and guidance are version-specific. |
