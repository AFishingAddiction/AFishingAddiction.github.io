---
layout: post
title: "Best Product Comparison Template for Bass Fishing"
permalink: /best-product-comparison-for-bass-fishing
excerpt: ""
author: dan
date: 2023-06-27T08:37:00-04:00
last_modified_at: 2023-06-27T08:37:00-04:00

image:
  path: /assets/img/posts/best-product-comparison-for-bass-fishing/dummy_800x800_000000_cccccc_replace-with-a-hero-image.png
  width: 800
  height: 800
  original_path: /assets/img/posts/best-product-comparison-for-bass-fishing/dummy_800x800_000000_cccccc_replace-with-a-hero-image.png
  original_width: 800
  original_height: 800
  alt: ""
  credit: ""
  render: true

tags:
  - bass
  - best
  - baits
seo:
  type: Article
related: []

lures:
  sub_category:
    - lure: Example Bait
      # Copied from the product page -> SiteStripe -> Image -> Medium
      image_link: <a href="https://www.amazon.com/Yum-Lures-YG365-Fishing-Silver/dp/B01MZZWF4P?crid=1S3RH6NCW90K9&keywords=fishing+lure&qid=1687913526&refinements=p_36%3A-300&rnid=386589011&sprefix=fishign+lure%2Caps%2C142&sr=8-3&linkCode=li2&tag=afishingaddict-20&linkId=68bcecbdedcf25e3144aa9dddaaa2b55&language=en_US&ref_=as_li_ss_il" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B01MZZWF4P&Format=_SL160_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=afishingaddict-20&language=en_US" ></a><img src="https://ir-na.amazon-adsystem.com/e/ir?t=afishingaddict-20&language=en_US&l=li2&o=1&a=B01MZZWF4P" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
      brand: Example
      type: Grub
      pieces: 1
      rating: 4.6
      rating_stars: <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half"></i>
      prime: true
      # Copied from the product page -> SiteStripe -> Text + Image (just the url of the iframe)
      iframe_link: "//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=afishingaddict-20&language=en_US&marketplace=amazon&region=US&placement=B01MZZWF4P&asins=B01MZZWF4P&linkId=a31fe3840950c01e31085c07396cc603&show_border=true&link_opens_in_new_window=true"
      # Examples: Best Rated, Best Value, Best Kit, Editor's Choice
      banner:
      # Options: primary, secondary, tertiary, quaternary
      banner_class: primary
      # A list of aggregated pros and cons directly from the review
      pros:
      cons:
    - banner:
      banner_class:
      lure:
      brand:
      rating:
      rating_stars: <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half"></i>
      iframe_link:
      # OR
      buy_url:
      image_link:
      prime:
      length:
      weight:
      type:
      hooks:
      blade_type:
      features:
        -
      pieces:
      summarized_reviews:
      pros:
        -
      cons:
        -
      personal_review:
---

INTRO PARAGRAPH TO ARTICLE

<h2>Table of Contents</h2>

- [Sub Category](#sub-category)

## Sub Category

INTRO PARAGRAPH TO SUB CATEGORY

{% for lure in page.lures.sub_category %}
  {% include product-table.md product=lure %}
{% endfor %}
<hr/>