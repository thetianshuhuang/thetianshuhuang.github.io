{% for item in service -%}
- **{{ item.name }}** &mdash; {{ item.description }}
{% endfor %}
