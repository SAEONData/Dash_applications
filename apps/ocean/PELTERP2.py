import pathlib
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app

station = 'PELTERP2'

# import Data into a .csv
csv_path = pathlib.Path(__file__).parent / 'Data' / 'dataframe.csv'
df = pd.read_csv(csv_path)

# list the variables we want to display
sensor_list = ['Conductivity', 'Temperature', 'Salinity', 'Oxygen', 'pH', 'Chlorophyll', 'Turbidity', 'Pressure']

#Subset the dataframe to only include the data from a single station
df = df.loc[df['Station'] == station]

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
    html.H1(station),
    # Dropdown for the variables to chart
    html.Label([
        "Select a Variable",
        dcc.Dropdown(
            id='var-dropdown', clearable=False,
            value='Temperature', options=[
                {'label': s, 'value': s}
                for s in sensor_list
            ])
    ]),
    # timeslider to analyse time series
    html.Label([
        "Select date range",
        dcc.RangeSlider(
            id='slider',
            marks=date_mark,
            min=0,
            max=22,
            value=[0, 2])
    ]),
    # Chart
    dcc.Graph(id= station + 'graph'),
    html.Div(id= station + '-display-value'),
])


# Define callback to update graph
@app.callback(
    Output(station + 'graph', 'figure'),
    [Input("var-dropdown", "value"),
     Input("slider", "value")
     ])

# define the function to update the graph based on the user selection
def update_figure(input1, input2):
    # Filter the Data by station
    data = df[(df.date > dates[input2[0]]) & (df.date < dates[input2[1]])]
    # update the plot
    fig = px.scatter(
        data,
        x="Depth",
        y=input1,
        color=input1,
        color_continuous_scale="Plasma",
        title=station
    )
    return fig


@app.callback(
    Output(station + '-display-value', 'children'),
    Input("var-dropdown", 'value')
)
def display_value(input1):
    return 'the variable being displayed in the chart is "{}"'.format(input1) + ' for the station ' + station
