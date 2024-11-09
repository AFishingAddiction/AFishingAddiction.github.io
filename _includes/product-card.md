{% assign orientationClassName = include.orientation | default: "responsive" %}

<!-- *BEGIN INCLUDE* -->

<!-- *Orientation: {{ include.orientation | default: "undefined" }}* -->

<!-- *Orientation Class: {{ orientationClassName }}* -->

<div class="product-card {{ orientationClassName }}">
    <a href="{{ include.product.text-link }}" target="_blank"><img src="{{ include.product.img-src }}" alt="{{ include.product.title }}" class="product-image"></a>
    <div class="product-info">
        <div class="product-title">{{ include.product.title }}</div>
        <div class="product-price">{{ include.product.price }}</div>
        <a href="{{ include.product.text-link }}" class="product-button" target="_blank">Buy Now</a>
    </div>
</div>
<!-- *END INCLUDE* -->