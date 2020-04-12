---
layout: default
title: "Bass Fishing Blog"
excerpt: "Recent blog posts about my fishing adventures in Ohio and some tips for landing the big ones"
permalink: /
seo:
  type: "Website"
---
<div class="posts">
  <h1>{{ page.title }}</h1>
  <h2>Popular Pages</h2>
  <div class="popular-pages-container">
    {% for doc in site.documents %}
    {% if doc.tags contains "top" %}
    <div class="popular-page">
      <h3><a href="{{ doc.url}}">{{ doc.title }}</a></h3>
      {{ doc.description | default: doc.excerpt }}
      <p><a class="btn btn-secondary" href="{{ doc.url}}" role="button">View details »</a></p>
    </div>
    {% endif %}
    {% endfor %}
  </div>
  {% for post in site.posts %}
    <article class="post">

      <h2><a href="{{ site.baseurl }}{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a></h2>

      {% include post_tags.html post_tags=post.tags %}

      <div class="entry">
        {{ post.excerpt }}
      </div>

      <a href="{{ site.baseurl }}{{ post.url }}" class="read-more" title="Read More of this Post">Read More</a>
    </article>
  {% endfor %}
</div>
