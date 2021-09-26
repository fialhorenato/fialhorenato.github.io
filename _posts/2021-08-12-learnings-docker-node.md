---
title: Learning from using Docker and Node - EXDEV Error
tags: Docker Technology
style: fill
color: danger
description: Possible problems by using Node and NPM inside a Docker image
layout: post
---

As part of a gig, i had to work with Dockerfile that install and build a Node project (Angular 9+).

Today in this post, i'll try to share my challenges and more painful discoveries while trying to make this project to work with Node and Docker.

Here is the list!

## EXDEV : cross-device link not permitted

If you try to update or install any npm dependency in an image that already have npm installed (any node images)

```
docker run node:latest npm install/update -g npm
```

You will probably experience this error.

Being more specific, this errors happens whenever NPM tries to use `fs.rename`.

A smart and clever solution, found by @nordluf on [github](https://github.com/npm/npm/issues/9863) is this:

```
RUN mv ./node_modules ./node_modules.tmp \
  && mv ./node_modules.tmp ./node_modules \
  && npm install 
```

The solution is kind of "hacky" but makes sense after all. The problem happens inside the filesystem for Docker. Docker filesystem is layered, and the union of those layers gives the complete picture of the Docker's image filesystem.

When you try to use `fs.rename` on this filesystem, Docker tries to copy all the data that it wants to use to the current layer from the read-only layer to perform the `fs.rename`. And since the operation require data from another read-only layer below and recursively, this is a very expensive operation.

Then, Docker aborts the operation throwing an EXDEV error, and since your application does not know how to handle this error, it ends up.

## Containers are stateless and have ephemeral storage!

Docker containers don't keep state, and if you want to move from A to B, you will potentially lose any changes done to the container.

You should always try to commit any container required files to the code repository, or generate them during the build time of the image.

If you need to have sensitive information, try to use ENV variables.

