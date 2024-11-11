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
{% assign imageClassName = "" %}
{% if include.product.add-image-buffer == true %}
    {% assign imageClassName = imageClassName | append: " pad" %}
{% endif %}
{% assign priceText = include.product.price | default: "Check Price" %}
{% if include.product.amazon-asin %}
    {% assign buttonText = "Buy on Amazon" %}
{% else %}
    {% assign buttonText = "Buy Now" %}
{% endif %}
{% assign debugEnabled = include.debug | default: false %}

{% if debugEnabled %}
*---BEGIN product-card.md INCLUDE---*

- *Orientation: {{ include.orientation | default: "undefined" }}*
- *Product Amazon ASIN: "{{ include.product.amazon-asin | default: "" }}"*
- *Product Price: "{{ include.product.price | default: "" }}"*
- *Product Banner Label: {% if include.product.banner-label != null %}"{{ include.product.banner-label }}"{% else %}undefined{% endif %}*
- *Include Banner Label: {% if include.banner-label != null %}"{{ include.banner-label }}"{% else %}undefined{% endif %}*
- *Banner Label: "{{ bannerLabel | default: "" }}"*
- *Add Image Buffer: "{{ include.product.add-image-buffer | default: "" }}"*
- *Image CSS Classes: {{ imageClassName }}*
- *CSS Classes: {{ cardClassName }}*
{% endif -%}

<div class="product-card {{ cardClassName }}">
    {% if bannerLabel != false %}<div class="product-label-banner">{{ bannerLabel }}</div>{% endif %}
    <a href="{{ include.product.text-link }}" target="_blank"><img src="{{ include.product.img-src }}" alt="{{ include.product.title | escape }}" class="product-image {{ imageClassName }}"></a>
    <div class="product-info">
        <div class="product-title">{{ include.product.title }}</div>
        <div class="product-price">{{ priceText }}</div>
        <a href="{{ include.product.text-link }}" class="product-button" target="_blank">{{ buttonText }}</a>
    </div>
</div>
{% if debugEnabled %}
*---END product-card.md INCLUDE---*
{% endif %}