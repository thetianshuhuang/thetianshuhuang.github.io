{% for award in awards %}
<span class="pill{% if award.emph %} pill-strong{% endif %}">{{ award.tag }}</span>
{%- if award.date -%}
<span class="pill-light">{{ award.date }}</span>
{%- endif -%}
**{{ award.title }}**
: {{ award.desc }}
{% endfor %}
