---
layout: default
title: "Some Recent Blog Posts"
excerpt: "Recent blog posts about my fishing adventures in Ohio and some tips for landing the big ones"
permalink: /
seo:
  type: 'Website'
---

<div class="posts">
  <h1>{{ page.title }}</h1>
  <p>Here are some blog posts I've written with fishing tips and stories of recent fishing trips that have satisfied my fishing addiction.</p>
  {% for post in site.posts %}
    <article class="post">

      <h2><a href="{{ site.baseurl }}{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a></h2>

      <div class="date">
        Written on {{ post.date | date: "%B %e, %Y" }} by {{ site.data.authors[post.author].name }}
      </div>
      {% include post_tags.html post_tags=post.tags %}

      <div class="entry">
        {{ post.excerpt }}
      </div>

      <a href="{{ site.baseurl }}{{ post.url }}" class="read-more" title="Read More of this Post">Read More</a>
    </article>
  {% endfor %}
</div>
