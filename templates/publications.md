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
<br>{{ paper.venue_long if paper.venue_long else paper.venue }}
{%- if paper.comment -%}
<span class="sep">&bullet;</span>{{ paper.comment }}
{%- endif -%}"

    {% if paper.summary -%}
    {{ paper.summary }}
    {{"{"}}: #{{label}} {{"}"}}
    {%- endif %}

    {% if paper.resources -%}
    {%- for name, url in paper.resources.items() -%}
    <a href="{{ url }}" target="_blank"><span style="margin-right: 16px; font-size: 14px" class="button">{{ name }}</span></a>
    {%- endfor -%}
    {%- endif %}

    {% if paper.figure -%}
    ![{{ paper.title }}](assets/research/{{ paper.figure }}){ width="1000" }
    {%- endif -%}

{% endfor %}
