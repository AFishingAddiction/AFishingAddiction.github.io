{% if page.related and page.related != empty %}
<div class="related-pages-container">
<h4>You May Also Like</h4>

<div class="related-pages">
{%- assign maxRelated = 3 %}
{%- assign minCommonTags = page.relatedMinCommonTags | default: 1 %}
{%- assign maxRelatedCounter = 0 %}
{%- assign all_pages = site.posts | concat: site.pages %}

{%- for coll in site.collections %}
  {%- for _page in site[coll.label] %}
    {%- assign all_pages = all_pages | push: _page %}
  {%- endfor %}
{%- endfor %}

  {%- for _page in all_pages %}

    {%- assign sameTagCount = 0 %}
    {%- assign commonTagsText = '' %}

    {%- for tag in _page.tags %}
      {%- if _page.url != page.url %}
        {%- if page.related %}
          {%- if page.related contains _page.url %}
            {%- assign sameTagCount = 999999 %}
            {%- assign commonTagsText = commonTagsText | append: tag | append: "|" %}
          {%- endif %}

        {%- elsif page.tags contains tag %}
          {%- assign sameTagCount = sameTagCount | plus: 1 %}
          {%- assign commonTagsText = commonTagsText | append: tag | append: "|" %}
        {%- endif %}
      {%- endif %}
    {%- endfor %}

    {%- if sameTagCount >= minCommonTags %}
      {%- assign maxRelatedCounter = maxRelatedCounter | plus: 1 %}
      {%- assign commonTagsList = commonTagsText | split: "|" %}
      <div class="related-page">
        <h5><a href="{{ site.baseurl }}{{ _page.url }}">{{ _page.title }}</a></h5>
        {% include post_tags.html post_tags=commonTagsList %}
        <p>{{ _page.description | default: _page.excerpt | strip_html | strip }}</p>
      </div>
      {%- if maxRelatedCounter >= maxRelated %}
        {%- break %}
      {%- endif %}
    {%- endif %}

  {%- endfor %}
</div>
</div>
{%- endif -%}