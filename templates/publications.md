{% for label, paper in publications.items() %}

??? {{ paper.tag }} "
{%- if paper.url -%}
[**{{ paper.title }}**]({{ paper.url }})
{%- else -%}
**{{ paper.title }}**
{%- endif -%}
<br>
{%- for author in paper.authors -%}
[{{ author }}][?]{% if not loop.last %}, {% endif %}{%- endfor -%}
<br>{{ paper.venue_long if paper.venue_long else paper.venue }}"

    {% if paper.summary -%}
    {{ paper.summary }}
    {{"{"}}: #{{label}} {{"}"}}
    {%- endif %}

    {% if paper.resources -%}
    {%- for name, url in paper.resources.items() -%}
    <span style="padding-right: 24px">[[{{ name }}]]({{ url }})</span>
    {%- endfor -%}
    {%- endif %}

    {% if paper.figure -%}
    ![{{ paper.title }}](assets/research/{{ paper.figure }}){ width="1000" }
    {%- endif -%}

{% endfor %}
