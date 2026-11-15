---
layout: splash
lang: en
locale: en_US
translation_url: /pt/
title: "Software Engineer in Amsterdam"
description: "Software engineer at Booking.com in Amsterdam writing about Java, Spring Boot, distributed systems, developer tools, AI, and lessons from building reliable software."
permalink: /
excerpt: "I’m Renato, a software engineer at Booking.com in Amsterdam. I write about software, engineering, and what I learn along the way."
---

<div class="home-intro">
  <p class="eyebrow">Software engineer · Amsterdam</p>
  <h1>Building reliable software.<br><em>Sharing what I learn.</em></h1>
  <p class="home-lede">I’m Renato, a software engineer at Booking.com in Amsterdam. I write about software, engineering, and the lessons I pick up along the way.</p>
  <div class="home-actions">
    <a class="btn btn--primary" href="/about/">About me</a>
    <a class="text-link" href="/blog/">Explore the blog <span aria-hidden="true">↗</span></a>
    <a class="text-link" href="/pt/" lang="pt-BR">Português</a>
  </div>
</div>

<section class="home-section">
  <div class="section-heading">
    <div>
      <p class="eyebrow">Ideas from the work</p>
      <h2>Recent articles</h2>
    </div>
    <a class="text-link" href="/blog/">View all articles <span aria-hidden="true">→</span></a>
  </div>
  <div class="recent-posts">
    {% assign recent_posts = site.posts | where: "lang", "en" | slice: 0, 3 %}
    {% for post in recent_posts %}
    <article class="recent-post">
      <p class="post-date">{{ post.date | date: "%b %Y" }}</p>
      <div>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        {% if post.description %}<p>{{ post.description }}</p>{% endif %}
      </div>
      <span class="post-arrow" aria-hidden="true">↗</span>
    </article>
    {% endfor %}
  </div>
</section>

<section class="home-note">
  <p class="eyebrow">What I’m exploring</p>
  <p>Distributed systems, developer tools, clear technical writing, and the small decisions that make software easier to trust and maintain.</p>
</section>
