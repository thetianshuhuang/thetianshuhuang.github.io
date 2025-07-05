import re
from typing import cast

import yaml
from jinja2 import Template
from mkdocs.config import Config
from mkdocs.config import config_options as opt
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


class CollaboratorsConfig(Config):
    name = "Tianshu Huang"
    index = opt.Type(str, default='data/people.yaml')


class CollaboratorsPlugin(BasePlugin[CollaboratorsConfig]):

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        plugin_cfg = cast(
            CollaboratorsConfig,
            config.plugins['collaborators'].config)  # type: ignore
        with open(plugin_cfg.index) as f:
            self.collaborators = yaml.safe_load(f)["people"]

        return config

    def on_page_markdown(
        self, markdown: str, /, *, page: Page,
        config: MkDocsConfig, files: Files
    ) -> str:
        plugin_cfg = cast(
            CollaboratorsConfig,
            config.plugins['collaborators'].config)  # type: ignore

        def replace_pattern(match: re.Match[str]) -> str:
            name = match.group(1).split(":")[0]
            if name == plugin_cfg.name:
                return f"**{name}**"
            elif name in self.collaborators:
                url = self.collaborators[name]
                return f"[{name}]({url})"
            else:
                return name

        pattern = re.compile(r"\[([^\[\]]*?)\]\[\?\]")
        return pattern.sub(replace_pattern, markdown)


class PublicationsConfig(Config):
    index = opt.Type(str, default='data/research.yaml')


class PublicationsPlugin(BasePlugin[PublicationsConfig]):

    template = (
        # Summary / header
        '??? {{ paper.tag }} "'
        '{% if paper.url %}'
        '[**{{ paper.title }}**]({{ paper.url }})'
        '{% else %}'
        '**{{ paper.title }}**'
        '{% endif %}'
        '<br>'
        '{% for author in paper.authors %}'
        '[{{ author }}][?]'
        '{% if not loop.last %}, {% endif %}'
        '{% endfor %}'
        '<br>'
        '{{ paper.venue_long if paper.venue_long else paper.venue }}'
        '"\n\n'
        # Expandable body...
        #   Summary
        '{% if paper.summary %}    {{ paper.summary }}\n\n{% endif %}'
        #   Resources
        '{% if paper.resources %}'
        '    '
        '{% for name, url in paper.resources.items() %}'
        '<span style="padding-right: 24px">[[{{ name }}]]({{ url }})</span>'
        '{% endfor %}'
        '\n\n'
        '{% endif %}'
        #   Figure
        '{% if paper.figure %}'
        '    ![{{ paper.title }}]({{ paper.figure }}){ width="1000" }\n\n'
        '{% endif %}'
    )

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        plugin_cfg = cast(
            PublicationsConfig,
            config.plugins['publications'].config)  # type: ignore
        with open(plugin_cfg.index) as f:
            self.publications = yaml.safe_load(f)["papers"]

        return config

    def on_page_markdown(
        self, markdown: str, /, *, page: Page,
        config: MkDocsConfig, files: Files
    ) -> str:
        if "::: publications" not in markdown:
            return markdown

        template = Template(self.template)

        publications = []
        for paper in self.publications.values():
            publications.append(template.render(paper=paper))

        publications_md = "".join(publications)

        return markdown.replace("::: publications", publications_md)
