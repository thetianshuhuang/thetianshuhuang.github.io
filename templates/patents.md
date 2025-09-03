{% for patent in patents %}
<span class="pill">{{ patent.status }}</span> **{{ patent.name }}**
<br>
{{ patent.date }}
<span class='sep'>&bullet;</span> {{ patent.number }}
<span class='sep'>&bullet;</span> {{ patent.assignee }}
{% endfor %}
