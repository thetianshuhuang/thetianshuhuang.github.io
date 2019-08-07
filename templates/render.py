from jinja2 import Template
import pandas as pd
import os
import json


def render(target, context=[], path=[], title=None, process_context=None):

    with open(target) as f:
        template = Template(f.read())
    with open('base.html') as f:
        base = Template(f.read())

    context = {
        f: pd.read_csv(os.path.join('definitions', f + '.csv'))
        for f in context
    }

    if process_context is not None:
        context = process_context(context)

    with open(os.path.join('..', target), 'w') as res:
        res.write(template.render(
            base=base,
            path=path,
            pagetitle="" if title is None else " | " + title,
            **context))


def get_folder_desc(folder):
    with open(os.path.join(folder, 'desc.txt')) as f:
        return f.read()


def get_images(ctx):

    return {
        "projects": [
            {
                "name": project["name"],
                "date": project["date"],
                "desc": get_folder_desc(
                    os.path.join("..", "renders", project["folder"])),
                "folder": project["folder"],
                "images": [
                    f for f in
                    os.listdir(
                        os.path.join("..", "renders", project["folder"]))
                    if f != 'desc.txt'
                ]
            } for _, project in ctx["architecture"].iterrows()
        ]
    }


def get_project_desc(name):
    with open(os.path.join('definitions', 'project_descriptions', name)) as f:
        return f.readlines()


def nan_to_null(x):
    if pd.isnull(x):
        return None
    else:
        return x


with open('definitions/tags.json') as f:
    TAGS = json.loads(f.read())

TAGS_ALL = {}
for k, v in TAGS.items():
    TAGS_ALL.update(v)


def tag_class_map(t):
    # PyPI -> use same tag
    if t.startswith('PyPI'):
        return 'tag-pypi'
    # Normal tag
    elif t in TAGS_ALL:
        return 'tag-' + t
    # Unrecognized tag -> misc
    else:
        print("Warning: Unrecognized Tag:", t)
        return ''


def tag_display_map(t):
    try:
        disp = TAGS_ALL[t]
    except KeyError:
        disp = t
    return disp.replace(" ", "&nbsp;")


def get_primary_tag(tags):
    return tag_class_map(tags.split(',')[0]).split('-')[1]


def get_descriptions(ctx):
    return {
        "projects": [
            {
                "name": project["name"],
                "organization": nan_to_null(project["organization"]),
                "icon": nan_to_null(project["icon"]),
                "tags": [
                    tag_display_map(t) for t in project["tag"].split(',')
                ],
                "primary_tag": get_primary_tag(project["tag"]),
                "tag_names": ' '.join(
                    [tag_class_map(t) for t in project["tag"].split(',')]),
                "link": project["link"],
                "desc": get_project_desc(project["description"])
            } for _, project in ctx["projects"][::-1].iterrows()
        ],
        "available_tags": TAGS,
        "tag_list": list(TAGS_ALL.keys()),
    }


if __name__ == '__main__':
    render(
        "panoramas.html",
        title="Panoramas",
        context=["panoramas"],
        path=[
            ['photography.html', 'Photography'],
            ['panoramas.html', 'Panoramas']
        ])
    render(
        "photos.html",
        title="Photos",
        context=["photos"],
        path=[
            ['photography.html', 'Photography'],
            ['photos.html', 'Photos']
        ])
    render(
        "photography.html",
        title="Photography",
        path=[['photography.html', 'Photography']])
    render(
        "architecture.html",
        title="Architecture",
        context=["architecture"],
        path=[['architecture.html', 'Architecture']],
        process_context=get_images)
    render(
        "miscellaneous.html",
        title="Miscellaneous",
        path=[['miscellaneous.html', 'Miscellaneous']])
    render("index.html")
    render(
        "resources.html",
        title="Resources",
        context=["resources"],
        path=[['resources.html', 'Resources']])
    render(
        "projects.html",
        title="Projects",
        context=['projects'],
        path=[['projects.html', 'Projects']],
        process_context=get_descriptions)
    render(
        "index.html", title="Tianshu Huang", context=[], path=[])
