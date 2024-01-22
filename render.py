import yaml
import os
from jinja2 import Template


TEMPLATE_PATH = "template"
TEMPLATE_BASE = "template/page.html"

with open(TEMPLATE_BASE) as f:
    base = Template(f.read())


context = {}
for path in os.listdir("data"):
    with open(os.path.join("data", path)) as f:
        context.update(yaml.load(f, Loader=yaml.Loader))


targets = {
    "index.html": None,
    "photography.html": "Photography"
}

for target, title in targets.items():
    with open(os.path.join(TEMPLATE_PATH, target)) as f:
        template = Template(f.read())
    contents = template.render(**context)
    extras = {"pagefile":  target, "pagetitle": title, "contents": contents}
    with open(target, 'w') as f:
        rendered = base.render(**context, **extras)
        f.write(rendered)
