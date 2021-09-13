import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

data = {
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five'
}

layout = html.Div([
    html.H1('Hello World!'),
    dcc.Slider(id='demo-slider', min=1, max=5, value=1),
    html.H3(data[1], id='demo-text')
])


@app.callback(
    Output('demo-text', 'children'),
    Input('demo-slider', 'value')
)
def update_layout(input_value):
    return data[input_value]
