---
layout: none
sitemap: false
---
var store = [
  {%- assign english_posts = site.posts | where: "lang", "en" -%}
  {%- for doc in english_posts -%}
  {
    "title": {{ doc.title | jsonify }},
    "excerpt": {{ doc.content | newline_to_br | replace:"<br />", " " | replace:"</p>", " " | replace:"</h1>", " " | replace:"</h2>", " " | replace:"</h3>", " " | replace:"</h4>", " " | replace:"</h5>", " " | replace:"</h6>", " " | strip_html | strip_newlines | jsonify }},
    "categories": {{ doc.categories | jsonify }},
    "tags": {{ doc.tags | jsonify }},
    "url": {{ doc.url | relative_url | jsonify }}
  }{% unless forloop.last %},{% endunless %}
  {%- endfor -%}
];
