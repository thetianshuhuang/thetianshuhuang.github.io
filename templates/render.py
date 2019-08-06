from jinja2 import Template
import pandas as pd
import os


def render(target, context=[], path=[]):

    with open(target) as f:
        template = Template(f.read())
    with open('base.html') as f:
        base = Template(f.read())

    context = {f: pd.read_csv(f + '.csv') for f in context}

    with open(os.path.join('..', target), 'w') as res:
        res.write(template.render(base=base, path=path, **context))


if __name__ == '__main__':
    render(
        "panoramas.html",
        context=["panoramas"],
        path=[
            ['photography.html', 'Photography'],
            ['panoramas.html', 'Panoramas']
        ])
    render(
        "photos.html",
        context=["photos"],
        path=[
            ['photography.html', 'Photography'],
            ['photos.html', 'Photos']
        ])
    render(
        "photography.html",
        path=[['photography.html', 'Photography']])
    render(
        "architecture.html",
        path=[['architecture.html', 'Architecture']])
    render(
        "miscellaneous.html",
        path=[['miscellaneous.html', 'Miscellaneous']])
    render("index.html")
    render(
        "resources.html",
        context=["resources"],
        path=[['resources.html', 'Resources']])
