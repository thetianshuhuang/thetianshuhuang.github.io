import yaml
import os
from jinja2 import Template


TEMPLATE_PATH = "template"
TEMPLATE_BASE = "template/page.html"
PAPER_TEMPLATE = "template/paper.html"
PAPERS_DIR = "papers"

with open(TEMPLATE_BASE) as f:
    base = Template(f.read())


context = {}
for path in os.listdir("data"):
    with open(os.path.join("data", path)) as f:
        context.update(yaml.load(f, Loader=yaml.Loader))


def _linkto(name: str, mode: str = 'simple') -> str:
    name, affiliations, *_ = (name + ':').split(':')

    if mode != 'full':
        affiliations = '*' if '*' in affiliations else ''
        if mode == 'cv' and name.startswith('Tianshu Huang'):
            return f'<b>{name}{affiliations}</b>'
    else:
        affiliations = affiliations.replace('*', "&#x1F7B1;")

    try:
        res = f'<a href="{context["people"][name]}">{name}</a>'
    except KeyError:
        res = name

    if len(affiliations) > 0:
        res += f"<sup>{affiliations}</sup>"
    return res


context["ref"] = _linkto
targets = {
    "index.html": None,
    "photography.html": "Photography",
    "504.html": "Not Available"
}

for target, title in targets.items():
    with open(os.path.join(TEMPLATE_PATH, target)) as f:
        template = Template(f.read())
    contents = template.render(**context)
    extras = {"pagefile":  target, "pagetitle": title, "contents": contents}
    rendered = base.render(**context, **extras)
    with open(target, 'w') as f:
        f.write(rendered)

with open(PAPER_TEMPLATE) as f:
    template = Template(f.read())

for paper in os.listdir(PAPERS_DIR):
    paper_context = context["papers"][paper.split('.')[0]]

    with open(os.path.join(PAPERS_DIR, paper)) as f:
        content = f.read()

    rendered = template.render(contents=content, **paper_context, **context)

    with open(paper, 'w') as f:
        f.write(rendered)
