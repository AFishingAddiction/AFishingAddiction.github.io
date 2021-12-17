---
layout: page
title: Posts by Tags
description: A list of tags and posts for each of A Fishing Addiction blog post.
permalink: /tags/
author: false
seo:
  type: Website
---

{%- assign tag_names = "" | split: "|" %}
{%- assign all_pages = site.posts | concat: site.pages %}

{%- for posts_by_tag in site.tags %}
  {%- assign  tag_names = tag_names | push: posts_by_tag.first %}
{%- endfor %}

{%- for coll in site.collections %}
  {%- for _page in site[coll.label] %}
    {%- assign all_pages = all_pages | push: _page %}
    {%- if _page.tags %}
      {%- assign tag_names = tag_names | concat: _page.tags %}
    {%- endif %}
  {%- endfor %}
{%- endfor %}

{% assign tag_names = tag_names | uniq | sort %}

{% include tag_list.html tag_names=tag_names %}

<hr>

<section class="posts-by-tags">
  {% for tag_name in tag_names %}
    <div id="{{ tag_name | slugify }}" class="tag-anchor"></div>
    <div>
      <h3>
        {{ tag_name | capitalize | replace: "_", " " }}
      </h3>
      {%- assign pages_with_tag = "" | split: "|" %}
      {%- for _page in all_pages %}
        {%- if _page.tags contains tag_name %}
          {%- assign pages_with_tag = pages_with_tag | push: _page %}
        {%- endif %}
      {%- endfor %}

      {%- for _page in pages_with_tag %}
      <div>
        <a href="{{ _page.url | prepend: baseurl }}">
          {{ _page.title }}
        </a>
      </div>
      {%- endfor %}
    </div>
  {%- endfor %}
</section>
