from jinja2 import Template
import pandas as pd
import os


def render(target, context=[]):

    with open(target) as f:
        template = Template(f.read())
    with open('base.html') as f:
        base = Template(f.read())

    context = {f: pd.read_csv(f + '.csv') for f in context}

    with open(os.path.join('..', target), 'w') as res:
        res.write(template.render(base=base, **context))


if __name__ == '__main__':
    render("photography.html", context=["landscapes", "panoramas"])
    render("architecture.html")
    render("miscellaneous.html")
    render("index.html")
