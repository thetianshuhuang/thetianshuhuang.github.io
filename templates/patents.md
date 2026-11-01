{% for patent in patents %}
<span class="pill{% if patent.emph %} pill-strong{% endif %}">{{ patent.status }}</span> **{{ patent.name }}**
<br>
{{ patent.date }}
<span class='sep'>&bullet;</span> {{ patent.number }}
<span class='sep'>&bullet;</span> {{ patent.assignee }}
{% endfor %}
