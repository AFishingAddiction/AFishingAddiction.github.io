---
layout: page
permalink: /tools/lure-wizard/
redirect_from: /tools/lure-picker/
title: Lure Wizard
author: false
excerpt: "A Fishing Addiction's Lure Wizard (free) provides up to 8 suggested lures and colors based on 3 questions: season, water clarity/visibility, and frontal status."
image:
  path: /assets/img/tools/Lure-Wizard-screenshot.png
  height: 860
  width: 552
  alt: Screenshot of A Fishing Addiction's Lure Wizard with pre-filled answers
  render: false
seo:
  type: WebApplication
  json_ld:
    aggregateRating:
      "@type": AggregateRating
      ratingValue: "5"
      ratingCount: "1"
    applicationCategory: ReferenceApplication
    audience: bass anglers
    browserRequirements: requires JavaScript
    creativeWorkStatus: beta
    creator:
      "@type": Person
      givenName: Daniel
      familyName: Schaefer
    keywords: "fishing lure picker, fishing lure wizards, what fishing lure to use"
    maintainer:
      "@type": Person
      givenName: Daniel
      familyName: Schaefer
    name: Lure Wizard
    operatingSystem: Any
    offers:
      "@type": "Offer"
      price: "0"
      priceCurrency: "USD"
    screenshot: "SITE_URL/IMAGE_PATH/tools/Lure-Wizard-screenshot.png"
    timeRequired: PT1M
is_comments_enabled: true
is_inline_ads_enabled: false
---
{%- if site.github.pages_env == "production" -%}
  {% assign assets_version = site.time | date: '%s%N' %}
{%- else -%}
  {% assign assets_version = site.github.pages_env %}
{%- endif %}
<link rel="stylesheet" type="text/css" href="{{ site.baseurl }}/assets/css/lure-picker.min.css?{{ assets_version }}" />
<script src="{{ site.baseurl }}/assets/js/lure-picker.min.js?{{ assets_version }}" async></script>
<noscript> You need to enable JavaScript to run this app. </noscript>
<div id="LurePicker"></div>

A Fishing Addiction's Lure Wizard asks a few simple questions and provides you with suggestions for lures to use. It asks for the season, water clarity and visibility, and the clous coverage or frontal status. With just those 3 questions, we are able to provide you with up to 8 different types of lures and the recommended color.

I want to improve the Lure Wizard based on feedback from users. Please comment below and let me know what you think about the Lure Wizard. The comments you enter are only for me and will not be published.