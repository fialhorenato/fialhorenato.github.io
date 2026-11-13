---
title: "Fixing npm EXDEV Errors in Docker Containers"
tags:
  - Docker
  - Node.js
  - npm
description: Troubleshoot npm EXDEV cross-device rename errors during Docker image builds and dependency installation.
last_modified_at: 2026-11-13
layout: single
---

While working on a project, I used a Dockerfile to install dependencies and build an Angular 9 application. This post records an EXDEV error I encountered and the workaround I tried. Docker and npm behavior can vary by version and build setup, so treat this as a troubleshooting example rather than a universal fix.

## What the npm EXDEV error means

If you try to update or install any npm dependency in an image that already have npm installed (any node images)

```
docker run node:latest npm install/update -g npm
```

You will probably experience this error.

More specifically, this error can occur when npm tries to rename a file across filesystem boundaries. A rename is atomic only within the same filesystem, so crossing that boundary can produce `EXDEV` (cross-device link).

One workaround suggested in this [npm issue](https://github.com/npm/npm/issues/9863) was to move the directory before installing:

```
RUN mv ./node_modules ./node_modules.tmp \
  && mv ./node_modules.tmp ./node_modules \
  && npm install 
```

The solution is kind of "hacky" but makes sense after all. The problem happens inside the filesystem for Docker. Docker filesystem is layered, and the union of those layers gives the complete picture of the Docker's image filesystem.

When you try to use `fs.rename` on this filesystem, Docker tries to copy all the data that it wants to use to the current layer from the read-only layer to perform the `fs.rename`. And since the operation require data from another read-only layer below and recursively, this is a very expensive operation.

Then, Docker aborts the operation throwing an EXDEV error, and since your application does not know how to handle this error, it ends up.

## Keep container builds reproducible

Containers are replaceable, so build-time dependencies should be reproducible from source and lockfiles. Generate required artifacts during the image build or include them in the build context. Pass secrets at runtime through an appropriate secret-management mechanism; don’t bake them into the image.

