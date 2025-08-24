import os
import re
from typing import cast
import logging

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
        '{% if paper.summary %}'
        '    {{ paper.summary }}\n'
        '    {{"{"}}: #{{label}} {{"}"}}\n\n'
        '{% endif %}'
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
        '    ![{{ paper.title }}](assets/research/{{ paper.figure }}){ width="1000" }\n\n'
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
        for label, paper in self.publications.items():
            publications.append(template.render(paper=paper, label=label))

        publications_md = "".join(publications)

        return markdown.replace("::: publications", publications_md)


class PhotosConfig(Config):
    index = opt.Type(str, default='data/photos.yaml')


class PhotosPlugin(BasePlugin[PhotosConfig]):

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        plugin_cfg = cast(
            PhotosConfig,
            config.plugins['photos'].config)  # type: ignore

        return config

    def on_page_markdown(
        self, markdown: str, /, *, page: Page,
        config: MkDocsConfig, files: Files
    ) -> str:
        if "::: photos" not in markdown:
            return markdown

        with open(os.path.join(os.path.dirname(__file__), 'photos.html')) as f:
            template = Template(f.read())

        plugin_cfg = cast(
            PhotosConfig,
            config.plugins['photos'].config)  # type: ignore

        with open(plugin_cfg.index) as f:
            data = yaml.safe_load(f)

        for section, photos in data["photos"].items():
            for photo in photos:
                photo['id'] = photo["path"].split('/')[-1].split('.')[0]

                lens = photo.get('lens')
                if '+' in lens:
                    lens, body = lens.split('+')
                else:
                    body = data['equipment']["default_cameras"].get(lens)

                photo['body'] = data['equipment']['cameras'].get(body, 'Unknown')
                photo['lens'] = data['equipment']['lenses'].get(lens, 'Unknown')

                if photo['body'] == "Unknown":
                    logging.warning(f"Unknown body for photo {photo['path']}: {body}")
                if photo['lens'] == "Unknown":
                    logging.warning(f"Unknown lens for photo {photo['path']}: {lens}")

                if "desc" in photo:
                    photo["desc"] = photo["desc"].replace('"', '&quot;')

        photos_md = ""
        for section, photos in data["photos"].items():
            photos_md += f"\n\n## {section}\n\n"
            photos_md += template.render(
                photos=photos, equipment=data['equipment'])

        return markdown.replace("::: photos", photos_md)
