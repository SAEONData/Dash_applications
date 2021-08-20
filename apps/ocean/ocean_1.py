import pathlib
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app

# import Data into a .csv
csv_path = pathlib.Path(__file__).parent / 'Data' / 'dataframe.csv'
df = pd.read_csv(csv_path)

# list the variables we want to display
sensor_list = ['Conductivity', 'Temperature', 'Salinity', 'Oxygen', 'pH', 'Chlorophyll', 'Turbidity', 'Pressure']

# Get a list of the Stations in alphabetical order
df = df.sort_values(by=['Station'])
stations = df['Station'].unique()

# Get a list of the dates we want to show
df['date'] = df['date'].replace('201900809', '20190809')
df = df.sort_values(by=['date', 'Depth'])
df['date'] = pd.to_datetime(df.date, format='%Y%m%d')
dates = df['date'].unique()
date_array = [str(i) for i in dates]
dates = [i[:10] for i in date_array]
date_mark = {i: dates[i] for i in range(0, 22)}

layout = html.Div([
    # Heading
    html.H1("Data Visualisation App"),
    # Subheading
    html.H2("Dynamic Visualisation of variables"),
    # Dropdown for the Station to chart
    html.Label([
        "Station",
        dcc.Dropdown(
            id='stat-dropdown', clearable=False,
            value='PELTERP1', options=[
                {'label': st, 'value': st}
                for st in stations
            ])
    ]),
    # timeslider to analyse time series
    html.Label([
        "Date",
        dcc.RangeSlider(
            id='slider',
            marks=date_mark,
            min=0,
            max=22,
            value=[0, 2])
    ]),
    # Chart
    dcc.Graph(id='graph'),
    # Dropdown for the variables to chart
    html.Label([
        "Variable",
        dcc.Dropdown(
            id='var-dropdown', clearable=False,
            value='Temperature', options=[
                {'label': s, 'value': s}
                for s in sensor_list
            ])
    ]),
    html.Div(id='app-2-display-value'),
])


# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("var-dropdown", "value"),
     Input("stat-dropdown", "value"),
     Input("slider", "value")
     ])
# define the function to update the graph based on the user selection
def update_figure(input1, input2, input3):
    # Filter the Data by station
    data = df[(df.date > dates[input3[0]]) & (df.date < dates[input3[1]])]
    # data = df.loc[df['Station'] ==input2]
    # update the plot
    fig = px.scatter(
        data.loc[data['Station'] == input2],
        x="Depth",
        y=input1,
        color=input1,
        color_continuous_scale="Plasma",
        title=input2
    )
    return fig


@app.callback(
    Output('app-2-display-value', 'children'),
    Input("var-dropdown", 'value'),
    Input("stat-dropdown", "value")
)
def display_value(input1, input2):
    return 'the variable being displayed in the chart is "{}"'.format(input1) + ' for the station "{}"'.format(input2)
