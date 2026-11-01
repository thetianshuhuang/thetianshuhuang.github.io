{% for student in students %}
<span class="pill{% if student.emph %} pill-strong{% endif %}">{{ student.from }} &mdash; {{ student.to }}</span>**{{ student.name }}** <span class="muted"><span class="sep">&bullet;</span>{{ student.level }}</span>
{%- if student.topic or student.next %}
: {% if student.topic -%}
{{ student.topic }}
{%- endif -%}
{%- if student.topic and student.next %}<br>{% endif -%}
{%- if student.next -%}
&xrarr; {{ student.next }}
{%- endif -%}
{%- endif %}
{% endfor %}
