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
from dash_extensions.javascript import assign
import dash_leaflet as dl
#external_stylesheets=[dbc.themes.GRID]
#directory = path.path(__file__).abspath()
#directory = pathlib.Path(__file__).parent.parent
#print(directory)
#from directory.app import app
from app import app

#app = dash.Dash(prevent_initial_callbacks=True)

def dicts_to_geojson(dicts, lat="lat", lon="lon"):
    geojson = {"type": "FeatureCollection", "features": []}
    for d in dicts:
        feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [d[lon], d[lat]]}}
        props = [key for key in d.keys() if key not in [lat, lon]]
        if props:
            feature["properties"] = {prop: d[prop] for prop in props}
        geojson["features"].append(feature)
    return geojson

style = {'width': '100%', 'height': '400px', 'float': 'left'}
#style2 = {'width': '49%', 'height': '500px', 'float': 'right'}

url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '


osmUrl = "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
osmUrlattribution = '<a href="http://openstreetmap.org">OpenStreetMap</a>'

googleUrl = "http://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
googleUrlattribution = "google"

esriUrl = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
esriUrlattribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"

Stadia_AlidadeSmooth = (
    "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png"
)
attribution_Stadia_AlidadeSmooth = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'

CartoDB_Positron = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
attribution_CartoDB_Positron = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'

# PELTER sites.
PELTER_sites = [dict(name="PELTER1", lat=-33.89616667, lon=25.70227778),
    dict(name="PELTER2", lat=-33.82624, lon=25.75429),
    dict(name="PELTER3", lat=-33.76805556, lon=25.90602778),
    dict(name="PELTER4", lat=-33.73205556, lon=26.06397222),
    dict(name="PELTER5", lat=-33.75666667, lon=26.23477778),
    dict(name="PELTER6", lat=-33.86869, lon=26.2914599999999),
    dict(name="PELTER7", lat=-33.88177, lon=25.98722),
    dict(name="PELTER8", lat=-34.034167, lon=25.727778)]

# Generate geojson with a marker for each city and name as tooltip.
geojson = dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in PELTER_sites])
# Create javascript function that filters out all PELTER_sites but PELTERP1.
geojson_filter = assign("function(feature, context){{return ['PELTERP1'].includes(feature.properties.name);}}")
point_to_layer = assign("""function(feature, latlng, context){
        // Figure out if the marker is selected
        //const match = context.props.hideout &&  context.props.hideout.properties.name === name;
        const match = context.props.hideout.includes(feature.properties.name);
        //const selected = context.props.hideout.includes(feature.properties.name);
        // Render selected markers in red.
        if(match){return L.circleMarker(latlng, {fillColor: 'green', fillOpacity: '0.75',Opacity: '1'});}
        //if(selected){return L.circleMarker(latlng, {fillColor: 'green', fillOpacity: '0.75',Opacity: '1'});}
        // Render non-selected markers in blue.
        //circleOptions.fillColor = 'red'
        return L.circleMarker(latlng, {fillColor: 'red', fillOpacity: '0.75',Opacity: '1'});
}""")


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
stations = ['PELTER1','PELTER2','PELTER3','PELTER4','PELTER5','PELTER6','PELTER7','PELTER8']
parquet_file = ""
# Get a list of the dates we want to show
#df['date'] = df['date'].replace('201900809', '20190809')
#df = df.sort_values(by=['date', 'Depth'])
#df['date'] = pd.to_datetime(df.date, format='%Y%m%d')
#dates = df['date'].unique()
#date_array = [str(i) for i in dates]
#dates = [i[:10] for i in date_array]
#date_mark = {i: dates[i] for i in range(0, 22)}
#/Users/privateprivate/SAEON/Dash_applications/assets/NRFSAEON.jpg
#image_filename = '/Users/privateprivate/SAEON/Dash_applications/assets/SAEON.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#c
layout = html.Div([
dbc.Card(
    dbc.CardBody([
        dbc.Row(children=[
            dbc.Col([
                html.Img(src=app.get_asset_url("NRFSAEON.jpg"), className='logo')
            ],width='auto'),
            dbc.Col([
                html.Img(src=app.get_asset_url("NMU.png"), className='logo')
            ],width='auto'),
            dbc.Col([
                html.Img(src=app.get_asset_url("CMR2.png"), className='logo')
            ],width='auto'),
            dbc.Col([
                html.Img(src=app.get_asset_url("CPUT.png"), className='logo')
            ],width='auto'),
            dbc.Col([
                html.Img(src=app.get_asset_url("GOAP.png"), className='logo')
            ],width='auto'),
        ],align="center"),
        
        
        
        
        dbc.Row(children=[
        # Left panel with site dropdown, map, and text description (3 rrows in a col
            dbc.Col(children=[
                dbc.Row(children=[
                    #Dropdown for the Station to chart
                    dbc.Col([
                        html.Label(["Station"])
                    ],width='auto'),
                    dbc.Col([
                        html.Label([
                            dcc.Dropdown(
                                id='stat-dropdown', clearable=False,
                                value='', options=[
                                    {'label': st, 'value': st}
                                    for st in stations
                                ])
                        ],style={'display': 'inline-block','margin-right': '2em','width':'80%','verticalAlign':'middle'}),
                    ],),
                ],align="center"),
                               
                #map
                dbc.Row(
                    html.Div([dl.Map([
                        dl.LayersControl([
                            dl.BaseLayer(dl.TileLayer(url=CartoDB_Positron,attribution=attribution_CartoDB_Positron,),
                                name="CartoDB.Positron",
                                checked="CartoDB.Positron" == "CartoDB.Positron",)]
                            + [dl.BaseLayer(dl.TileLayer(url=googleUrl, attribution=googleUrlattribution),
                                name="Google Sat",)]
                            + [dl.BaseLayer(dl.TileLayer(url=esriUrl, attribution=esriUrlattribution),name="Esri",)]
                            + [dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_50cm_MOSAIC",layers="CDNGI_Imagery_50cm_MOSAIC",format="image/png",transparent=True,)),name="CDNGI_Imagery_50cm_MOSAIC",)]
                            + [dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_25cm_MOSAIC_2017",layers="CDNGI_Imagery_25cm_MOSAIC_2017",format="image/png",transparent=True,)),name="CDNGI_Imagery_25cm_MOSAIC_2017",)]
                            + [dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_25cm_MOSAIC_2018",layers="CDNGI_Imagery_25cm_MOSAIC_2018",format="image/png",transparent=True,)),name="CDNGI_Imagery_25cm_MOSAIC_2018",)]), dl.GeoJSON(data=geojson,  cluster=True,zoomToBoundsOnClick=True,options=dict(pointToLayer=point_to_layer),
                                hideout=dict(click_feature=None),id="geojson"),
                    ],
                        zoom=9,
                        center=(-33.681, 25.842),
                        style=style,
                        id="map",
                    )
                    ])),
                dbc.Row(children=[
                    html.Div(["Lorem Ipsum"])
                ]),
                
                
            ],width=5),
            
            #right hand col
            dbc.Col(children=[
                dbc.Row(children=[
                    dbc.Col([
                        html.Label(["x variable"])
                    ],width='auto'),
                    dbc.Col([
                        html.Label([
                        dcc.Dropdown(
                            id='var-dropdownx', clearable=False,
                            value='', options=[
                                {'label': s, 'value': s}
                                for s in sensor_list
                            ]),
                        ],style={'display': 'inline-block','margin-right': '2em','width':'80%','verticalAlign':'middle'})
                    ]),
                ],align="center"),
                dbc.Row(children=[                    
                    dbc.Col([
                        html.Label(["y variable"])
                    ],width='auto'),
                    dbc.Col([
                        html.Label([
                        dcc.Dropdown(
                            id='var-dropdowny', clearable=False,
                            value='', options=[
                                {'label': s, 'value': s}
                                for s in sensor_list
                            ]),
                        ],style={'display': 'inline-block','margin-right': '2em','width':'80%','verticalAlign':'middle'})
                    ]),
                ],align="center"),
                
                
                
                
                
                dbc.Row(children=[
                    
                    html.Div(dcc.Graph(id='graph_new',style={'height': '400px'})),
                ]),
            ],width=7)
        ])
    ])
)
])

#app.layout = html.Div([
#   # Heading
#   html.H1("Datashader Visualisation App"),
#   # Subheading
##   html.H2("Dynamic Visualisation of variables"),
#   # Dropdown for the Station to chart
#   html.Label([
#       "Station",
#       dcc.Dropdown(
#           id='stat-dropdown', clearable=False,
#           value='', options=[
#               {'label': st, 'value': st}
#               for st in stations
#           ])
#           ],style={'display': 'inline-block', 'width': '25%','margin-right': '2em','verticalAlign':'middle'}),
##   # timeslider to analyse time series
##   html.Label([
##       "Date",
##       dcc.RangeSlider(
##           id='slider',
##           marks=date_mark,
##           min=0,
##           max=22,
##           value=[0, 2])
##   ]),
#   # Chart
#   
#   # Dropdown for the variables to chart
#   html.Label([
#       "x variable   ",
##       ,dcc.Checklist(['   reverse axis'],checked=False,
##           style={'display': 'inline-block','margin-right': '2em'},id='var-check-reversex'
##       ),
#       dcc.Dropdown(
#           id='var-dropdownx', clearable=False,
#           value='', options=[
#               {'label': s, 'value': s}
#               for s in sensor_list
#           ])
#   ],style={'display': 'inline-block', 'width': '25%','margin-right': '2em','verticalAlign':'middle'}),
#   html.Label([
#       "y variable   ",    
##       dcc.Checklist(['   reverse axis'],checked=True,id='var-check-reversey',
##           style={'display': 'inline-block','margin-right': '2em'}
##       ),
#
#       dcc.Dropdown(
#           id='var-dropdowny', clearable=False,
#           value='', options=[
#               {'label': s, 'value': s}
#               for s in sensor_list
#           ])
#   ],style={'display': 'inline-block', 'width': '25%','margin-right': '2em','verticalAlign':'middle'}),
#   
#   html.Div(dcc.Graph(id='graph_new',style={'height': '500px'})),
#   
#])
# Define callback to update graph

@app.callback([Output("map", "center"),Output("map", "zoom")], [Input("stat-dropdown", "value"), Input("geojson", "click_feature"),])
def func(input, feature):
    if not input or not feature:
        raise PreventUpdate        
    if input:
        for i in PELTER_sites:
            if str(input)==i['name']:
                lat=i['lat']
                lon=i['lon']        
        return [(lat, lon),9]
    
    if feature:
        lat = feature['geometry']['coordinates'][1]
        lon=feature['geometry']['coordinates'][0] 
        return [(lat, lon),9]
    
    
@app.callback(
    Output("geojson", "hideout"),
    Input("stat-dropdown", "value"),
    Input("geojson", "click_feature"),
    
)
def update_map( input,feature):
    return str(input)

@app.callback(
    Output("stat-dropdown", "value"),
    Input("geojson", "click_feature"),
    
)
def update_dropdown(feature):
    if not feature:
        pass
    try:
        opts = [str(feature['properties']['name'])]
        options=[{'label':opt, 'value':opt} for opt in opts]
        return str(feature['properties']['name'])
    except:
        pass
        

    
# Update the feature saved on the hideout prop on click.
#app.clientside_callback("function(feature){return feature}", Output("states", "hideout"), [Input("states", "click_feature")])
#
@app.callback(
    Output('graph_new', 'figure'),
    Input("stat-dropdown", "value"),
    Input("var-dropdownx", "value"),
    Input("var-dropdowny", "value")
    
)
## define the function to update the graph based on the user selection
def update_figure(input1, input2, input3):
##   print(input4)
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
        elif input1 == 'PELTER8':
            parquet_file = pathlib.Path(__file__).parent / 'Data' / 'pelter8.parquet'
            
            
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
            margin=dict(l=0, r=0, t=30, b=0),
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
    