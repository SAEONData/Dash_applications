import pathlib
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np
import datashader as ds
import datetime
import dash_bootstrap_components as dbc
import pyarrow.parquet as pq
#external_stylesheets=[dbc.themes.GRID]
#directory = path.path(__file__).abspath()
#directory = pathlib.Path(__file__).parent.parent
#print(directory)
#from directory.app import app
from app import app

#app = dash.Dash(prevent_initial_callbacks=True)


#app = dash.Dash(__name__,external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)
## import Data into a .csv
#csv_path = pathlib.Path(__file__).parent / 'apps' / 'ocean' / 'Data' /'dataframe.csv'
#
#df = pd.read_csv(csv_path)


##print(df)
##
## list the variables we want to display
sensor_list = ['ITime','Conductivity [uS/cm]', 'Temperature [ITS-90 deg C]', 'Depth [salt water m]', 'Salinity, Practical [PSU]', 'Oxygen (SBE 43) [mg/l]', 'pH [pH]', 'Chlorophyll (Turner Cyclops) [ug/l]', 'Turbidity (Turner Cyclops) [NTU]']
#
## Get a list of the Stations in alphabetical order
#df = df.sort_values(by=['Station'])
stations = ['PELTER1','PELTER2','PELTER3','PELTER4','PELTER5','PELTER6','PELTER7']
parquet_file = ""
# Get a list of the dates we want to show
#df['date'] = df['date'].replace('201900809', '20190809')
#df = df.sort_values(by=['date', 'Depth'])
#df['date'] = pd.to_datetime(df.date, format='%Y%m%d')
#dates = df['date'].unique()
#date_array = [str(i) for i in dates]
#dates = [i[:10] for i in date_array]
#date_mark = {i: dates[i] for i in range(0, 22)}

layout = html.Div([
    # Heading
    html.H1("Datashader Visualisation App"),
    # Subheading
#   html.H2("Dynamic Visualisation of variables"),
    # Dropdown for the Station to chart
    html.Label([
        "Station",
        dcc.Dropdown(
            id='stat-dropdown', clearable=False,
            value='', options=[
                {'label': st, 'value': st}
                for st in stations
            ])
            ],style={'display': 'inline-block', 'width': '25%','margin-right': '2em','verticalAlign':'middle'}),
#   # timeslider to analyse time series
#   html.Label([
#       "Date",
#       dcc.RangeSlider(
#           id='slider',
#           marks=date_mark,
#           min=0,
#           max=22,
#           value=[0, 2])
#   ]),
    # Chart
    
    # Dropdown for the variables to chart
    html.Label([
        "x variable",
        dcc.Dropdown(
            id='var-dropdownx', clearable=False,
            value='', options=[
                {'label': s, 'value': s}
                for s in sensor_list
            ])
    ],style={'display': 'inline-block', 'width': '25%','margin-right': '2em','verticalAlign':'middle'}),
    html.Label([
        "y variable",
        dcc.Dropdown(
            id='var-dropdowny', clearable=False,
            value='', options=[
                {'label': s, 'value': s}
                for s in sensor_list
            ])
    ],style={'display': 'inline-block', 'width': '25%','margin-right': '2em','verticalAlign':'middle'}),
    html.Div(dcc.Graph(id='graph_new',style={'height': '500px'})),
    
])
# Define callback to update graph
@app.callback(
    Output('graph_new', 'figure'),
    Input("stat-dropdown", "value"),
    Input("var-dropdownx", "value"),
    Input("var-dropdowny", "value")
    
)
# define the function to update the graph based on the user selection
def update_figure(input1, input2, input3):
    try:
        parquet_file=''
        if input1 == 'PELTER1':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter1.parquet'
            
        elif input1 == 'PELTER2':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter2.parquet'
        elif input1 == 'PELTER3':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter3.parquet'
        elif input1 == 'PELTER4':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter4.parquet'
        elif input1 == 'PELTER5':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter5.parquet'
        elif input1 == 'PELTER6':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter6.parquet'
        elif input1 == 'PELTER7':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter7.parquet'
            
            
        dq=pq.read_table(parquet_file,filters=[('Temperature [ITS-90 deg C]', '>', -10),('Temperature [ITS-90 deg C]', '<', 30)])
        df=dq.to_pandas()
        
        
        x=str(input2)
        x_range = (df.iloc[0][str(input2)], df.iloc[-1][str(input2)])
        
#       if input2 == 'ITime':
        datess_index=[]
        datess=[]
        numElems=10
        idx = np.round(np.linspace(x_range[0], x_range[1] - 1, numElems)).astype('int64')
        for i in idx:
            datess_index.append(i)
            datess.append(pd.to_datetime(i, format='%Y-%m-%d', errors='coerce').date())
        cvs = ds.Canvas(plot_width=256, plot_height=256)
#       else:
            
    #   print(input1, input2)
        y=str(input3)
        agg = cvs.points(df, x,y)
        
        zero_mask = agg.values == 0
        agg.values = np.log10(agg.values, where=np.logical_not(zero_mask))
        agg.values[zero_mask] = np.nan
        
        fig = px.imshow(agg, origin='lower', color_continuous_scale='turbo',labels={'color':'Log10(count)'})
        fig.update_traces(hoverongaps=False)
        fig.update_layout(coloraxis_colorbar=dict(title='Count'))
        
        
        if input2 == 'ITime':
            fig.update_xaxes(
                
                tickmode = 'array',
                tickvals=datess_index,
                ticktext=datess,
                title="time"
            )
        fig.update_layout(
            yaxis = dict(autorange="reversed")
        )
        return fig
    except:
        raise PreventUpdate


#@app.callback(
#   Output('app-2-display-value', 'children'),
#   Input("var-dropdown", 'value'),
#   Input("stat-dropdown", "value")
#)
#def display_value(input1, input2):
#   return 'the variable being displayed in the chart is "{}"'.format(input1) + ' for the station "{}"'.format(input2)
#

#if __name__ == '__main__':
#   app.run_server(debug=True)
    