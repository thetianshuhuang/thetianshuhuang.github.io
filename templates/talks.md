<div class="grid cards" markdown>
{% for talk in talks %}

- {% if talk.url -%}
[**{{ talk.title }}**]({{ talk.url }})
{%- else -%}
**{{ talk.title }}**
{%- endif -%}
<br>
{%- if talk.comment -%}
{{ talk.comment }}
<br>
{%- endif -%}
{{ talk.location }}

{% endfor %}
</div>
