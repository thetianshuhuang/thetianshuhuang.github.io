{% for award in awards %}
<span class="pill">{{ award.tag }}</span>
{%- if award.date -%}
<span class="pill-light">{{ award.date }}</span>
{%- endif -%}
**{{ award.title }}**
: {{ award.desc }}
{% endfor %}
