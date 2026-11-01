{% for class in teaching %}
<span class="pill{% if class.emph %} pill-strong{% endif %}">{{ class.type }}</span><span class="pill-light">{{ class.date}}</span>**{{ class.title }}**
: {% for line in class.desc -%}
{{ line }}
{% if not loop.last %}<br>{% endif %}
{%- endfor -%}

{% endfor %}
