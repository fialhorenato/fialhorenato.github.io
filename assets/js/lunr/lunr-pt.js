---
layout: null
sitemap: false
---
var idx = lunr(function () {
  this.field('title');
  this.field('excerpt');
  this.field('categories');
  this.field('tags');
  this.ref('id');

  // Lunr's default stemmer and stop-word list are English-specific.
  this.pipeline.remove(lunr.stopWordFilter);
  this.pipeline.remove(lunr.stemmer);
  this.searchPipeline.remove(lunr.stopWordFilter);
  this.searchPipeline.remove(lunr.stemmer);

  for (var item in store) {
    this.add({
      title: store[item].title,
      excerpt: store[item].excerpt,
      categories: store[item].categories,
      tags: store[item].tags,
      id: item
    });
  }
});

$(document).ready(function () {
  $('input#search').on('keyup', function () {
    var resultdiv = $('#results');
    var query = $(this).val().toLowerCase();
    var result = idx.query(function (q) {
      query.split(lunr.tokenizer.separator).forEach(function (term) {
        if (!term) return;
        q.term(term, { boost: 100 });
        if (query.lastIndexOf(' ') !== query.length - 1) {
          q.term(term, { usePipeline: false, wildcard: lunr.Query.wildcard.TRAILING, boost: 10 });
        }
        q.term(term, { usePipeline: false, editDistance: 1, boost: 1 });
      });
    });
    resultdiv.empty();
    resultdiv.prepend('<p class="results__found">' + result.length + ' resultado(s) encontrado(s)</p>');
    result.forEach(function (match) {
      var post = store[match.ref];
      var excerpt = post.excerpt.split(' ').slice(0, 20).join(' ') + '...';
      resultdiv.append('<div class="list__item"><article class="archive__item"><h2 class="archive__item-title"><a href="' + post.url + '" rel="permalink">' + post.title + '</a></h2><p class="archive__item-excerpt">' + excerpt + '</p></article></div>');
    });
  });
});
