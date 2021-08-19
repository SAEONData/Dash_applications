import pathlib
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


from app import app
app_list = []

file_path = pathlib.Path(__file__).parent.parent

for dir_, _, files in os.walk(file_path):
    for file_name in files:
        if file_name.endswith(".py"):
            if file_name.endswith("__init__.py"):
                pass
            elif file_name.endswith(".py"):
                rel_dir = os.path.relpath(dir_, file_path)
                name = file_name[:-3]
                app_string = '/apps/'+ rel_dir + '/' + name
                app_list.append(app_string)

layout = html.Div([
    # Heading
    html.H1("Welcome to the SAEON Dash applications page"),
    # Subheading
    html.H2("list of Application urls"),
    #Table of Contents
    html.Ul([html.Li(x) for x in app_list])
    ])