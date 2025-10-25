import logging
import os
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


class TemplateConfig(Config):
    templates = opt.Dir(default="./templates")
    context = opt.Dir(default="./data")


class TemplatePlugin(BasePlugin[TemplateConfig]):

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        plugin_cfg = cast(
            TemplateConfig,
            config.plugins['template'].config)  # type: ignore

        self.pattern = re.compile(
            r"::: (((?P<context>\w+)@(?P<template>\w+))|(?P<template_only>\w+))")

        return config

    def on_page_markdown(
        self, markdown: str, /, *, page: Page,
        config: MkDocsConfig, files: Files
    ) -> str:
        plugin_cfg = cast(
            TemplateConfig,
            config.plugins['template'].config)  # type: ignore

        rendered = {}
        for match in re.finditer(self.pattern, markdown):

            if match.group("template_only") is not None:
                template_file = f'{match.group("template_only")}.md'
                context_file = f'{match.group("template_only")}.yaml'
            else:
                template_file = f'{match.group("template")}.md'
                context_file = f'{match.group("context")}.yaml'
            
            with open(os.path.join(plugin_cfg.templates, template_file)) as f:
                template = Template(f.read())
            with open(os.path.join(plugin_cfg.context, context_file)) as f:
                context = yaml.safe_load(f.read())

            rendered[match.group(0)] = template.render(**context)

        for pattern, rendered in rendered.items():
            markdown = markdown.replace(pattern, rendered)
        return markdown
