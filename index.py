import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    from apps import app1, app2

    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
