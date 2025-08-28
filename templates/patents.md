{% for patent in patents %}
<span class="pill">{{ patent.status }}</span> **{{ patent.name }}**
<br>
{{ patent.date }} &nbsp;&nbsp;&bullet;&nbsp;&nbsp;  {{ patent.number }} &nbsp;&nbsp;&bullet;&nbsp;&nbsp;{{ patent.assignee }}
{% endfor %}
