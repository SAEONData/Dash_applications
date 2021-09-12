import importlib
import os
import pathlib

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps.contents import contents

# expose the Flask instance for the HTTP server (gunicorn)
server = app.server

# create a pathlist for the various dash apps
file_path = pathlib.Path(__file__).parent / 'apps'

# Scan through the apps directory and find all the dash apps
projlist = []
modlist = []

for dir_, _, files in os.walk(file_path):
    for file_name in files:
        if file_name.endswith(".py"):
            if file_name.endswith("__init__.py"):
                pass
            # add them to the lists
            elif file_name.endswith(".py"):
                rel_dir = os.path.relpath(dir_, file_path)
                projlist.append(rel_dir)
                name = file_name[:-3]
                modlist.append(name)

# Import app modules and map them to URL paths
path_module_mapping = {}
for i in range(len(projlist)):
    path_module_mapping['/apps/' + projlist[i] + '/' + modlist[i]] = importlib.import_module('apps.' + projlist[i] + '.' + modlist[i])

# Build the layout of the index page
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return contents.layout
    try:
        module = path_module_mapping[pathname]
        return module.layout
    except KeyError:
        return '404'


if __name__ == '__main__':
    # Start the Flask server for local development
    app.run_server(debug=True)
