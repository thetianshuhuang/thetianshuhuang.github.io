{% for talk in talks %}
{% if talk.type %}<span class="pill{% if talk.emph %} pill-strong{% endif %}">{{ talk.type }}</span> {% endif %}
{%- if talk.url -%}
[**{{ talk.title }}**]({{ talk.url }})
{%- else -%}
**{{ talk.title }}**
{%- endif %}
<br>
{{ talk.location }}
{%- if talk.comment %}
<span class='sep'>&bullet;</span> {{ talk.comment }}
{%- endif %}
{% endfor %}
