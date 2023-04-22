{% assign lure = include.product %}
<div class="comparison-table">
  {% if lure.banner %}
  <span class="banner {{ lure.banner_class }}">{{ lure.banner }}</span>
  {% endif %}
  <div class="row">
    <div class="head">Photo</div>
    <div class="data">{{ lure.image_link }}</div>
  </div>
  <div class="row">
    <div class="head">Lure</div>
    <div class="data">{{ lure.lure }}</div>
  </div>
  <div class="row">
    <div class="head">Brand</div>
    <div class="data">{{ lure.brand }}</div>
  </div>
  {% if lure.hooks %}
  <div class="row">
    <div class="head">Hook Type</div>
    <div class="data">{{ lure.hooks }}</div>
  </div>
  {% endif %}
  {% if lure.type %}
  <div class="row">
    <div class="head">Lure Type</div>
    <div class="data">{{ lure.type }}</div>
  </div>
  {% endif %}
  {% if lure.blade_type %}
  <div class="row">
    <div class="head">Blade Type</div>
    <div class="data">{{ lure.blade_type }}</div>
  </div>
  {% endif %}
  {% if lure.weight %}
  <div class="row">
    <div class="head">Weight</div>
    <div class="data">{{ lure.weight }}</div>
  </div>
  {% endif %}
  {% if lure.length %}
  <div class="row">
    <div class="head">Length</div>
    <div class="data">{{ lure.length }}</div>
  </div>
  {% endif %}
  <div class="row">
    <div class="head">Pieces</div>
    <div class="data">{{ lure.pieces }}</div>
  </div>
  <div class="row">
    <div class="head">Rating</div>
    <div class="data">{{ lure.rating }} {{ lure.rating_stars }}</div>
  </div>
  <div class="row">
    <div class="head">Prime</div>
    <div class="data">{% if lure.prime %}Yes{% else %}No{% endif %}</div>
  </div>
  {% if lure.summarized_reviews %}
  <div class="row">
    <div class="head">Summary of Reviews</div>
    <div class="data">
      <ul>
        {% for summary in lure.summarized_reviews %}
        <li>{{ summary }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  {% if lure.pros %}
  <div class="row">
    <div class="head">Pros</div>
    <div class="data">
      <ul>
        {% for pro in lure.pros %}
        <li>{{ pro }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  {% if lure.cons %}
  <div class="row">
    <div class="head">Cons</div>
    <div class="data">
      <ul>
        {% for con in lure.cons %}
        <li>{{ con }}</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  <div class="row">
    <div class="head">Buy</div>
    <div class="data"><iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="{{ lure.iframe_link }}"></iframe></div>
  </div>
</div>