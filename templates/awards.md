{% for award in awards %}
<span class="pill">{{ award.tag }}</span> **{{ award.title }}**
{%- if award.date -%}
<span class="sep">&bullet;</span>{{ award.date }}
{%- endif %}
: {{ award.desc }}
{% endfor %}
