---
layout: splash
lang: pt-BR
locale: pt_BR
title: "Engenheiro de Software em Amsterdã"
description: "Renato Fialho é engenheiro de software na Booking.com, em Amsterdã. Escreve sobre Java, Spring Boot, sistemas distribuídos, ferramentas e engenharia de software."
permalink: /pt/
translation_url: /
excerpt: "Sou Renato, engenheiro de software na Booking.com, em Amsterdã. Escrevo sobre software, engenharia e o que aprendo no caminho."
---

<div class="home-intro">
  <p class="eyebrow">Engenheiro de software · Amsterdã</p>
  <h1>Construindo software confiável.<br><em>Compartilhando aprendizados.</em></h1>
  <p class="home-lede">Sou Renato, engenheiro de software na Booking.com, em Amsterdã. Escrevo sobre software, engenharia e as lições que aprendo no trabalho.</p>
  <div class="home-actions">
    <a class="btn btn--primary" href="/pt/about/">Sobre mim</a>
    <a class="text-link" href="/pt/blog/">Explorar os artigos <span aria-hidden="true">↗</span></a>
    <a class="text-link" href="/" lang="en">English</a>
  </div>
</div>

<section class="home-section">
  <div class="section-heading">
    <div>
      <p class="eyebrow">Ideias do trabalho</p>
      <h2>Artigos recentes</h2>
    </div>
    <a class="text-link" href="/pt/blog/">Ver todos os artigos <span aria-hidden="true">→</span></a>
  </div>
  <div class="recent-posts">
    {% assign recent_posts = site.posts | where: "lang", "pt-BR" | slice: 0, 3 %}
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
  <p class="eyebrow">Temas que estou explorando</p>
  <p>Sistemas distribuídos, ferramentas para desenvolvedores, escrita técnica e decisões que tornam o software mais confiável e fácil de manter.</p>
</section>
