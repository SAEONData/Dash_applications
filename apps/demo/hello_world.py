import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

data = {
    1: 'One',
    2: 'Two',
    3: 'Three'
}

layout = html.Div([
    html.H1('Hello World!'),
    dcc.Slider(id='demo-slider', min=1, max=3, value=1),
    html.H3(data[1], id='demo-text')
])


@app.callback(
    Output('demo-text', 'children'),
    Input('demo-slider', 'value')
)
def update_layout(slider_value):
    return data[slider_value]
