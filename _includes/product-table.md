{% assign product = include.product %}
### {{ product.lure | default: product.product }}
<div class="comparison-table">
  {% if product.banner %}
  <span class="banner {{ product.banner_class }}">{{ product.banner }}</span>
  {% endif %}
  <div class="row">
    <div class="head">Image</div>
    <div class="data">{{ product.image_link }}</div>
  </div>
  <div class="row">
    <div class="head">Buy</div>
    <div class="data">
    {% if product.iframe_link -%}
      <iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="{{ product.iframe_link }}"></iframe>
    {%- else if product.buy_url -%}
      <a class="btn btn-accent" href="{{ product.buy_url }}" role="button">Check Price »</a>
    {%- endif %}
    </div>
  </div>
  {% if product.lure -%}
  <div class="row">
    <div class="head">Lure</div>
    <div class="data">{{ product.lure }}</div>
  </div>
  {%- endif %}
  {% if product.product -%}
  <div class="row">
    <div class="head">Product</div>
    <div class="data">{{ product.product }}</div>
  </div>
  {%- endif %}
  <div class="row">
    <div class="head">Brand</div>
    <div class="data">{{ product.brand }}</div>
  </div>
  {% if product.type %}
  <div class="row">
    <div class="head">Lure Type</div>
    <div class="data">{{ product.type }}</div>
  </div>
  {% endif %}
  {% if product.hooks %}
  <div class="row">
    <div class="head">Hook Type</div>
    <div class="data">{{ product.hooks }}</div>
  </div>
  {% endif %}
  {% if product.blade_type %}
  <div class="row">
    <div class="head">Blade Type</div>
    <div class="data">{{ product.blade_type }}</div>
  </div>
  {% endif %}
  {% if product.weight %}
  <div class="row">
    <div class="head">Weight</div>
    <div class="data">{{ product.weight }}</div>
  </div>
  {% endif %}
  {% if product.length %}
  <div class="row">
    <div class="head">Length</div>
    <div class="data">{{ product.length }}</div>
  </div>
  {% endif %}
  {% if product.color %}
  <div class="row">
    <div class="head">Color</div>
    <div class="data">{{ product.color }}</div>
  </div>
  {% endif %}
  {% if product.size %}
  <div class="row">
    <div class="head">Size</div>
    <div class="data">{{ product.size }}</div>
  </div>
  {% endif %}
  {% if product.features %}
  <div class="row">
    <div class="head">Features</div>
    <div class="data">
      <ul>
        {% for feature in product.features %}
        <li>{{ feature }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  <div class="row">
    <div class="head">Pieces</div>
    <div class="data">{{ product.pieces }}</div>
  </div>
  <div class="row">
    <div class="head">Rating</div>
    <div class="data">{{ product.rating }} {{ product.rating_stars }}</div>
  </div>
  {% if product.prime %}
  <div class="row">
    <div class="head">Prime</div>
    <div class="data">Yes</div>
  </div>
  {% endif %}
  {% if product.pros %}
  <div class="row">
    <div class="head">Pros</div>
    <div class="data">
      <ul>
        {% for pro in product.pros %}
        <li>{{ pro }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  {% if product.cons %}
  <div class="row">
    <div class="head">Cons</div>
    <div class="data">
      <ul>
        {% for con in product.cons %}
        <li>{{ con }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  <div class="row">
    <div class="head">Buy</div>
    <div class="data">
    {% if product.iframe_link -%}
      <iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="{{ product.iframe_link }}"></iframe>
    {%- else if product.buy_url -%}
      <a class="btn btn-accent" href="{{ product.buy_url }}" role="button">Check Price »</a>
    {%- endif %}
    </div>
  </div>
</div>
{% if product.summarized_reviews %}
#### Summary of the Reviews
  {{ product.summarized_reviews | markdownify }}
{% endif %}
{% if product.personal_review %}
#### Personal Review
  {{ product.personal_review | markdownify }}
{% endif %}
<hr/>