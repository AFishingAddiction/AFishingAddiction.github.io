---
layout: default
title: Bass Fishing Blog
excerpt: "Recent blog posts about my fishing adventures in Ohio and some tips for landing the big ones"
permalink: /
author: false
img:
  path: /logo/A-Fishing-Addiction-logo.png
seo:
  type: Website
---
<div class="posts">
  <h1>{{ page.title }}</h1>
  <div class="lure-wizard-promo">
    <h2><a href="/tools/lure-wizard/">Try the New Lure Wizard</a></h2>
    <p>
    A Fishing Addiction's new <a href="/tools/lure-wizard/">Lure Wizard</a> is a browser tool that asks you, the angler, 3 simple questions about the current fishing conditions. The <a href="/tools/lure-wizard/">Lure Wizard</a> then provides you with several options or suggestions for lures to use in those conditions.
    </p>
    <p>Click the image below to get started.</p>
    <p><a href="/tools/lure-wizard/"><img src="/{{ '/tools/Lure-Wizard-screenshot.png' | prepend: site.static.image.path }}" alt="A Fishing Addiction's Lure Wizard" /></a></p>
    <p><a class="btn btn-accent" href="/tools/lure-wizard/" role="button">Try Lure Wizard now »</a></p>
  </div>
  <div class="popular-pages-container">
    <h2>Popular Pages</h2>
    <div class="popular-pages">
    {% for doc in site.documents -%}
    {% if doc.tags contains "top" %}
    <div class="popular-page">
      <h3><a href="{{ doc.url}}">{{ doc.title }}</a></h3>
      <p>{{ doc.description | default: doc.excerpt }}</p>
      <p><a class="btn btn-secondary" href="{{ doc.url}}" role="button">View details »</a></p>
    </div>
    {% endif %}
    {%- endfor %}
    </div>
  </div>
  {% include ads/inline-content.html %}
  {% for post in site.posts %}
    {% if post.canonical_url == nil %}
    <article class="post">
      <h2><a href="{{ site.baseurl }}{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a></h2>

      {% include post_tags.html post_tags=post.tags %}

      <div class="entry">
        <p>{{ post.excerpt | strip_html | strip }}</p>
      </div>

      <a href="{{ site.baseurl }}{{ post.url }}" class="read-more" title="Read More of this Post">Read More</a>
    </article>
    {% endif %}
  {% endfor %}
</div>
