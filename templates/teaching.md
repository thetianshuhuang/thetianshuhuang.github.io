{% for class in teaching %}
<span class="pill">{{ class.type }}</span> **{{ class.title }}**<span class="sep">&bullet;</span>{{ class.date}}
: {% for line in class.desc -%}
{{ line }}
{% if not loop.last %}<br>{% endif %}
{%- endfor -%}

{% endfor %}
