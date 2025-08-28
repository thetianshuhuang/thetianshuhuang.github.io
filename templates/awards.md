{% for award in awards %}
<span class="pill">{{ award.date }}</span>{{ award.title }}
: {{ award.desc }}
{% endfor %}
