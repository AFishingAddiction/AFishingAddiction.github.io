{% assign cardClassName = include.orientation | default: "responsive" %}
{% if include.product.banner-label != null %}
    {% assign bannerLabel = include.product.banner-label | default: "&nbsp;" %}
{% elsif include.banner-label != null %}
    {% assign bannerLabel = include.banner-label | default: "&nbsp;" %}
{% else %}
    {% assign bannerLabel = "Product Recommendation" %}
{% endif %}
{% if bannerLabel == false %}
    {% assign cardClassName = cardClassName | append: " no-banner" %}
{% endif %}
{% assign debugEnabled = include.debug | default: false %}

{% if debugEnabled %}
*---BEGIN product-card.md INCLUDE---*

- *Orientation: {{ include.orientation | default: "undefined" }}*
- *Product Banner Label: {% if include.product.banner-label != null %}"{{ include.product.banner-label }}"{% else %}undefined{% endif %}*
- *Include Banner Label: {% if include.banner-label != null %}"{{ include.banner-label }}"{% else %}undefined{% endif %}*
- *Banner Label: "{{ bannerLabel | default: "" }}"*
- *CSS Classes: {{ cardClassName }}*
{% endif -%}

<div class="product-card {{ cardClassName }}">
    {% if bannerLabel != false %}<div class="product-label-banner">{{ bannerLabel }}</div>{% endif %}
    <a href="{{ include.product.text-link }}" target="_blank"><img src="{{ include.product.img-src }}" alt="{{ include.product.title }}" class="product-image"></a>
    <div class="product-info">
        <div class="product-title">{{ include.product.title }}</div>
        <div class="product-price">{{ include.product.price }}</div>
        <a href="{{ include.product.text-link }}" class="product-button" target="_blank">Buy Now</a>
    </div>
</div>
{% if debugEnabled %}
*---END product-card.md INCLUDE---*
{% endif %}