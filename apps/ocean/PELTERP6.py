import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime
from app import app
from apps.ocean.Data.Ocean_Data_Loader import df
from apps.ocean.Data.Ocean_Data_Loader import season

sensor_list = ['Conductivity', 'Temperature', 'Salinity', 'Oxygen', 'pH', 'Chlorophyll', 'Turbidity', 'Pressure']
chart_list = ['scatter', 'box']
station = 'PELTERP6'

Data = df.loc[df['Station'] == station]

# Get a list of the dates we want to show
df = Data.sort_values(by=['date', 'Depth'])

layout = \
    dbc.Container(children=[
        # Header Row
        dbc.Row(children=[dbc.Col([html.H1(df['Station'].unique(), className='headerFont')]),
                          dbc.Col([html.Img(src=app.get_asset_url("SAEON.png"), className='logo')]),
                          dbc.Col([html.Img(src=app.get_asset_url("NMU_logo.png"), className='logo')]),
                          dbc.Col([html.Img(src=app.get_asset_url("CMR Logo 1_Blue Gold Transparent .png"),
                                            className='logo')]),
                          ], className='headerbox'),
        # Time Slider Row
        dbc.Row(children=[dbc.Col(children=[
            html.Label([
                "Select date range",
                dcc.RangeSlider(
                    id=station + 'slider',
                    min=0,
                    value=[0, 0],
                )]
            )],
            className='sliderbox'),
        ]),
        # Chart and other boxes Row
        dbc.Row(children=[
            # Chart Column
            dbc.Col(children=[dcc.Graph(id=station + 'graph',
                                        style={'width': '100%'})],
                    className='box'),
            # Other Stuff Column
            dbc.Col(children=[
                # Season Selector Row
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Label(['Select a Season',
                                    dcc.Checklist(
                                        id='season-selector',
                                        options=[{'label': k, 'value': k} for k in season.keys()],
                                        value=['spring'])],
                                   )],
                        className='box')
                ]),
                # Variable Dropdown Row
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Label(["Select a Variable",
                                    dcc.Dropdown(
                                        id='var-dropdown',
                                        clearable=False,
                                        value='Temperature',
                                        options=[{'label': s, 'value': s} for s in sensor_list])],
                                   className='drop font')],
                        className='box'),
                ]),
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Label(["Select a Charting Style",
                                    dcc.Dropdown(
                                        id='char-dropdown',
                                        clearable=False,
                                        value='scatter',
                                        options=[{'label': c, 'value': c} for c in chart_list])],
                                   className='drop font')],
                        className='box'),
                ]),
                # text insert row
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Div(id=station + '-display-value',
                                 className='bodyFont')],
                        className='box'),
                ]),
                dbc.Row(children=[
                    dbc.Col(children=[
                        html.Button("Download Data", id="btn_csv", className='button'),
                        dcc.Download(id=station + "download-dataframe-csv"),
                    ])
                ]),
            ]),
        ]),
    ], className='backdrop')


# Define the callback to update dates list

@app.callback(
    Output(station + 'slider', 'marks'),
    Input('season-selector', 'value'))
def set_dates(selected_season):
    date_list = []
    for s in selected_season:
        date_list.append(season[s])
    flat_list = [item for sublist in date_list for item in sublist]
    flat_list.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d'))

    def listToDict(lst):
        op = {i: dict(label=lst[i], style={'transform': 'rotate(45deg)',
                                           'alignItems': 'left',
                                           'paddingTop': '1vh'}) for i in range(0, len(lst))}
        return op

    marks = listToDict(flat_list)
    return marks


@app.callback(
    Output(station + 'slider', 'max'),
    Input(station + 'slider', 'marks'))
def set_slider_min_value(available_options):
    max = len(available_options) - 1
    return max


# Define callback to update graph
@app.callback(
    Output(station + 'graph', 'figure'),
    [Input("var-dropdown", "value"),
     Input(station + "slider", "value"),
     Input('season-selector', 'value'),
     Input('char-dropdown', 'value')
     ])
# define the function to update the graph based on the user selection
def update_figure(input1, input2, input3, input4):
    # Filter the Data by Season
    if len(input3) == 4:
        season_data = df.loc[(df['season'] == input3[0]) | (df['season'] == input3[1]) | (df['season'] == input3[2]) | (
                df['season'] == input3[3])]
    elif len(input3) == 3:
        season_data = df.loc[(df['season'] == input3[0]) | (df['season'] == input3[1]) | (df['season'] == input3[2])]
    elif len(input3) == 2:
        season_data = df.loc[(df['season'] == input3[0]) | (df['season'] == input3[1])]
    else:
        season_data = df.loc[(df['season'] == input3[0])]
    # Filter the Data by date in slider
    dates = season_data['date'].unique()
    season_filter_data = season_data[(season_data.date >= dates[input2[0]]) & (season_data.date <= dates[input2[1]])]
    # update the plot
    if input4 == 'scatter':
        fig = px.scatter(
            season_filter_data,
            x=input1,
            y="Depth",
            labels=dict(Depth='Depth Below Surface (m)'),
            color=input1,
            color_continuous_scale="Plasma",
            title=station
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(autorange="reversed")
    else:
        fig = px.box(
            season_filter_data,
            x=input1,
            y="depth_class",
            labels=dict(depth_class='Classed depth below surface (m)'),
            color="depth_class",
            notched=True,
            # color=input1,
            # color_continuous_scale="Plasma",
            title=station
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(autorange="reversed")
    return fig


@app.callback(
    Output(station + '-display-value', 'children'),
    Input("var-dropdown", 'value')
)
def display_value(input1):
    return 'The variable being displayed in the chart is "{}"'.format(input1) + ' for the station ' + df[
        'Station'].unique()


@app.callback(
    Output(station + 'slider_display-value', 'children'),
    Input(station + "slider", "value")
)
@app.callback(
    Output(station + "download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "SAEON_AlgoaBay_CTD" + station + ".csv")
