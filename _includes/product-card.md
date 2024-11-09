{% assign orientationClassName = include.orientation | default: "responsive" %}
{% assign cardLabel = include.card-label | default: "Product Recommendation"}
{% assign debugEnabled = include.debug | default: false %}

{% if debugEnabled %}
*---BEGIN product-card.md INCLUDE---*

*Orientation: {{ include.orientation | default: "undefined" }}*

*Orientation Class: {{ orientationClassName }}*

*Include Label: {{ include.card-label | default: "undefined" }}*

*Label: {{ cardLabel }}*
{% endif -%}

<div class="product-card {{ orientationClassName }}">
    {% if cardLabel %}<div class="product-label-banner">{{ cardLabel }}</div>{% endif %}
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