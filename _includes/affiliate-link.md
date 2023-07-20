<span class="aff-link"><a href="{{ include.link.text-link }}" target="_blank">{{ include.content }}</a>
{%- if include.link.hover-html -%}
  <span class="hover-content">{::nomarkdown}
    {{- include.link.hover-html -}}
  {:/}</span>
{%- endif -%}
</span>