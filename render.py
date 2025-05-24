"""Render templates."""

import os

import tyro
import yaml
from jinja2 import Template


def _load_context(path: str = "data") -> dict:
    context = {}
    for path in os.listdir(path):
        with open(os.path.join("data", path)) as f:
            context.update(yaml.load(f, Loader=yaml.Loader))

    def _linkto(name: str, mode: str = 'simple') -> str:
        name, affiliations, *_ = (name + ':').split(':')

        if mode != 'full':
            affiliations = '*' if '*' in affiliations else ''
            if mode == 'cv' and name.startswith('Tianshu Huang'):
                return f'<b>{name}{affiliations}</b>'

        try:
            res = f'<a href="{context["people"][name]}">{name}</a>'
        except KeyError:
            res = name

        if len(affiliations) > 0:
            res += f"<sup>{affiliations}</sup>"
        return res

    context["ref"] = _linkto
    return context


def render(
    templates: str = "./template", papers: str = "./papers", data: str = "data"
) -> None:
    """Render website templates.

    Args:
        templates: template file directory.
        papers: paper sub-templates.
        data: data file directory.
    """
    TEMPLATE_BASE = os.path.join(templates, "page.html")
    PAPER_TEMPLATE = os.path.join(templates, "paper.html")

    with open(TEMPLATE_BASE) as f:
        base = Template(f.read())

    context = _load_context(data)
    targets = {
        "index.html": None,
        "photography.html": "Photography",
        "404.html": "Not Available"
    }

    for target, title in targets.items():
        with open(os.path.join(templates, target)) as f:
            template = Template(f.read())
        contents = template.render(**context)
        extras = {
            "pagefile":  target, "pagetitle": title, "contents": contents}
        rendered = base.render(**context, **extras)
        with open(target, 'w') as f:
            f.write(rendered)

    with open(PAPER_TEMPLATE) as f:
        template = Template(f.read())

    for paper in os.listdir(papers):
        paper_context = context["papers"][paper.split('.')[0]]

        with open(os.path.join(papers, paper)) as f:
            content = f.read()

        rendered = template.render(
            contents=content, **paper_context, **context)

        with open(paper, 'w') as f:
            f.write(rendered)


if __name__ == '__main__':
    tyro.cli(render)
