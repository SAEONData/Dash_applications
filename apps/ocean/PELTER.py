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
from datetime import datetime as dt
from datetime import date
#external_stylesheets=[dbc.themes.GRID]
#directory = path.path(__file__).abspath()
#directory = pathlib.Path(__file__).parent.parent
#print(directory)
#from directory.app import app
from app import app

#app = dash.Dash(prevent_initial_callbacks=True)
def f(row):
    if row['date'].month in range(3, 6):
        val = 'autumn'
    elif row['date'].month in range(6, 9):
        val = 'winter'
    elif row['date'].month in range(9, 12):
        val = 'spring'
    else:
        val = 'summer'
    return val

def dicts_to_geojson(dicts, lat="lat", lon="lon"):
    geojson = {"type": "FeatureCollection", "features": []}
    for d in dicts:
        feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [d[lon], d[lat]]}}
        props = [key for key in d.keys() if key not in [lat, lon]]
        if props:
            feature["properties"] = {prop: d[prop] for prop in props}
        geojson["features"].append(feature)
    return geojson

style = {'width': '100%', 'height': '350px', 'float': 'left'}
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
        const flag = L.icon({iconUrl: '/assets/star_red.png', iconSize: [16, 16]});
        const flag2 = L.icon({iconUrl: '/assets/star_green.png', iconSize: [16, 16]});
        //const selected = context.props.hideout.includes(feature.properties.name);
        // Render selected markers in red.
        if(match){return L.marker(latlng, {icon: flag2})};
        //L.circleMarker(latlng, {fillColor: 'green', fillOpacity: '0.75',Opacity: '1'});}
        //if(selected){return L.circleMarker(latlng, {fillColor: 'green', fillOpacity: '0.75',Opacity: '1'});}
        // Render non-selected markers in blue.
        //circleOptions.fillColor = 'red'
        return L.marker(latlng, {icon: flag}); 
        //L.circleMarker(latlng, {fillColor: 'red', fillOpacity: '0.75',Opacity: '1'});
}""")





#app = dash.Dash(__name__,external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)
## import Data into a .csv
#csv_path = pathlib.Path(__file__).parent / 'apps' / 'ocean' / 'Data' /'dataframe.csv'
#
#df = pd.read_csv(csv_path)


##print(df)
##
## list the variables we want to display
sensor_list = ['Chlorophyll-a (Turner Cyclops) [ug/l]','Conductivity [uS/cm]', 'Depth (sea water) [m]','Integer Time','Oxygen (SBE 43) [mg/l]', 'pH [pH]','Salinity [PSU]','Temperature (ITS-90) [deg C]', 'Turbidity (Turner Cyclops) [NTU]']

chart_types=['Heatmap (x,y variables)', 'Box plot (x variable)']
#Heat map display of log counts of data values/pixel.
stations = ['PELTER1','PELTER2','PELTER3','PELTER4','PELTER5','PELTER6','PELTER7','PELTER8']
parquet_file = ""

filter_table = pd.DataFrame({'Start':[],'End':[],'Min':[],'Max':[],'Summer':[], 'Spring':[], 'Autumn':[], 'Winter':[], 'Depth bins':[]})
seasonList=['Spring','Summer','Autumn','Winter']


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
            html.H2(["ODET: Ocean Data Explorer Tool"
                
            ],style={'display': 'inline-block','width':'100%','verticalAlign':'middle','textAlign': 'center'}),
        ],align="center"),
        dbc.Row(children=[
            html.H4(["Algoa Bay Sentinel Site CTD raw in-situ data, 2012 -2021"
                
            ],style={'display': 'inline-block','width':'100%','verticalAlign':'middle','textAlign': 'center'}),
        ],align="center"),
        
        
        
        dbc.Row(children=[
        # Left panel with site dropdown, map, and text description (3 rrows in a col
            dbc.Col(children=[
                dbc.Row(children=[
                    #Dropdown for the Station to chart
                    dbc.Col([
                        html.Label(["SELECT a Station:"],className = 'prepend-text')
                    ],width='auto'),
                    dbc.Col([
                        html.Label([
                            dcc.Dropdown(
                                id='stat-dropdown', clearable=False,
                                style={'height': '25px','width':'100%','display': 'inline-block'},
                                value='', options=[
                                    {'label': st, 'value': st}
                                    for st in stations
                                ])
                        ],className = 'append-text',style={'display': 'inline-block','width':'100%','verticalAlign':'middle'}),
                    ]),
                ],align="center"),
                    
        
                    
                    dbc.Row(children=[
                        dbc.Col([
                            html.Label(["SELECT x variable:"],className = 'prepend-text')
                        ],width='auto'),
                        dbc.Col([
                            html.Label([
                            dcc.Dropdown(
                                id='var-dropdownx', clearable=False,
                                style={'height': '25px','width':'100%','display': 'inline-block'},
                                value='Temperature (ITS-90) [deg C]', options=[
                                    {'label': s, 'value': s}
                                    for s in sensor_list
                                ])
                            ],className = 'append-text',style={'display': 'inline-block','width':'100%','verticalAlign':'middle'})
                        ]),
                    ],align="center"),
                    dbc.Row(children=[
                        dbc.Col([
                            html.Label(["SELECT y variable:"],className = 'prepend-text')
                        ],width='auto'),
                        dbc.Col([
                            html.Label([
                            dcc.Dropdown(
                                id='var-dropdowny', clearable=False,
                                style={'height': '25px','width':'100%','display': 'inline-block'},
                                value='Depth (sea water) [m]', options=[
                                    {'label': s, 'value': s}
                                    for s in sensor_list
                                ]),
                            ],className = 'append-text',style={'display': 'inline-block','width':'100%','verticalAlign':'middle'})
                        ]),
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
                        center=(-33.76805556, 25.90602778),
                        style=style,
                        id="map",
                    )
                    ])),
                dbc.Row(children=[
                    html.Div(['Collaborative tool development: Marc Pienaar, Erika Brown & Hayden Wilson'])
                ],className = 'append-text'),
                
                
            ],width=5),
            
            #right hand col
            dbc.Col(children=[
                dbc.Row(children=[
                    dbc.Col([
                        html.Label(["Chart type:"],className = 'prepend-text')
                        
                    ],width='auto'),
                    dbc.Col([
                        html.Label([
                        dcc.Dropdown(
                            id='var-chartTypeDropdown', clearable=False,
                            style={'height': '25px','width':'100%','display': 'inline-block'},
                            value='Heatmap (x,y variables)', options=[
                                {'label': s, 'value': s}
                                for s in chart_types
                            ])
                        ],className = 'append-text',style={'display': 'inline-block','width':'100%','verticalAlign':'middle'})
                    ]),
                    
                    dbc.Col([
                        html.Label([
                            dcc.Checklist(
                                id='reverse_x_axis',
                                options=[' Reverse x-axis'],
                                    value=['no']),
                                
                        ],className = 'prepend-text')
                    ],width='auto'),
                    
                    dbc.Col([
                        html.Label([
                            dcc.Checklist(
                                id='reverse_y_axis',
                                options=[' Reverse y-axis'],
                                    value=[' Reverse y-axis']),
                            
                        ],className = 'prepend-text')
                    ],width='auto'),
                    
                    
                    
                ],align="center"),
                
                dbc.Row(children=[
                    dbc.Col([
                    
                    html.Label(["Select a Season: ",
                        
                        
                        dcc.Checklist(
                            id='season_selector',
                            options=[{'label': k, 'value': k} for k in seasonList],
                            value=['Spring','Summer','Autumn','Winter'])
#                       dcc.RangeSlider(0, 20, 1, value=[5, 15], id='my-range-slider')
                        
                    ],className='append-text')
                    
                    ]),
                    dbc.Col([
                        
                            
                        dcc.DatePickerRange(
                            id='my-date-picker-range',                            
                            start_date=dt.strptime("2012-04-18", "%Y-%m-%d").date(),
                            end_date=dt.strptime("2021-03-16", "%Y-%m-%d").date(),
                            display_format="YYYY/MM/DD",
                            clearable=False,
                        )
                    
                    ])
                    
                ],align="center"),

                                          
                dbc.Row(children=[
                    html.Div(dcc.Graph(id='graph_new',style={'height': '400px'})),
                ]),
#               dbc.Row(children=[
#                   html.Label([
#                       'Collaborative tool development: Marc Pienaar, Erika Brown & Hayden Wilson'
#                   ]),
#                   
#               ]),
            ],width=7)
        ]),
        dbc.Row(children=[
            dbc.Col([
                html.Img(src=app.get_asset_url("NRFSAEON.jpg"), className='logo')
            ]),
            dbc.Col([
                html.Img(src=app.get_asset_url("NMU.png"), className='logo')
            ]),
            dbc.Col([
                html.Img(src=app.get_asset_url("CMR2.png"), className='logo')
            ]),
            dbc.Col([
                html.Img(src=app.get_asset_url("CPUT.png"), className='logo')
            ]),
            dbc.Col([
                html.Img(src=app.get_asset_url("GOAP.png"), className='logo')
            ]),
        ],align="center")
    ]),
    
)
])
# Define callback to update graph
#@app.callback(
#   Output('output-container-date-picker-range', 'children'),
#   Input('my-date-picker-range', 'start_date'),
#   Input('my-date-picker-range', 'end_date'))
#
#def update_output(start_date, end_date):
#   string_prefix = 'You have selected: '
#   if start_date is not None:
#       start_date_object = date.fromisoformat(start_date)
#       start_date_string = start_date_object.strftime('%B %d, %Y')
#       string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#   if end_date is not None:
#       end_date_object = date.fromisoformat(end_date)
#       end_date_string = end_date_object.strftime('%B %d, %Y')
#       string_prefix = string_prefix + 'End Date: ' + end_date_string
#   if len(string_prefix) == len('You have selected: '):
#       return 'Select a date to see it displayed here'
#   else:
#       return string_prefix



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
    Input("var-dropdowny", "value"),
    Input('reverse_y_axis', 'value'),
    Input('reverse_x_axis', 'value'),
    Input('var-chartTypeDropdown', 'value'),
    Input('season_selector', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
    
)
## define the function to update the graph based on the user selection
def update_figure(input1, input2, input3,input4,input5, input6,input7,date1,date2):
#   print(date1)
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
                        
#       dq=pq.read_table(parquet_file,columns=['Date','Date2','season','iTime',str(input2),str(input3)])
        dq=pq.read_table(parquet_file)#,filters=[('Temperature [ITS-90 deg C]', '>', -10),('Temperature [ITS-90 deg C]', '<', 30)])
        df=dq.to_pandas()
        #convert to datetime
        df['Date2'] = pd.to_datetime(df['Date2'], format='%Y-%m-%d').dt.date

        # Filter the Data by Season
        if len(input7) == 4:
            df = df.loc[(df['Season'] == input7[0]) | (df['Season'] == input7[1]) | (df['Season'] == input7[2]) | (
                df['Season'] == input7[3])]
        elif len(input7) == 3:
            df = df.loc[(df['Season'] == input7[0]) | (df['Season'] == input7[1]) | (df['Season'] == input7[2])]
        elif len(input7) == 2:
            df = df.loc[(df['Season'] == input7[0]) | (df['Season'] == input7[1])]
        else:
            df = df.loc[(df['Season'] == input7[0])]
        
        start_date_object = date.fromisoformat(date1)
        end_date_object = date.fromisoformat(date2)
        df = df[(df.Date2 >= start_date_object) & (df.Date2 <= end_date_object)]

                
        x=str(input2)
        x_range = (df.iloc[0][str(input2)], df.iloc[-1][str(input2)])
        datess_index=[]
        datess=[]
        numElems=5
        idx = np.round(np.linspace(x_range[0], x_range[1] - 1, numElems)).astype('int64')
        for i in idx:
            datess_index.append(i)
            datess.append(pd.to_datetime(i, format='%Y-%m-%d', errors='coerce').date())
        cvs = ds.Canvas(plot_width=256, plot_height=256)
        y=str(input3)
        
        
        
        if input6 == 'Heatmap (x,y variables)':
#           categorizer = ds.category_binning('val', lower=10, upper=50, nbins=4, include_under=False, include_over=False)
            
            agg = cvs.points(df, x,y)
#           nonzero_values = agg.value[0::] > 0
            
#           agg = agg.values[nonzero_values]
            zero_mask = agg.values == 0
            
#           print(agg.values[0])
            agg.values = np.trunc(agg.values, where=np.logical_not(zero_mask))
            agg.values[zero_mask]=np.nan
#           agg.values[zero_mask] = np.nan
#           
            fig = px.imshow(agg, origin='lower', color_continuous_scale='turbo',labels={'color':'Count'})
            fig.update_traces(hoverongaps=False)
            fig.update_layout(coloraxis_colorbar=dict(title='Count'))
            if input2 == 'Integer Time':
                fig.update_xaxes(
                    tickmode = 'array',
                    tickvals=datess_index,
                    ticktext=datess,
                    title="time"
                )
                
        else:
            fig = px.box(
                df, 
                x=str(input2),
                y="depth_class",
                color="Season",
                color_discrete_map={ # replaces default color mapping by value
                    "Summer": "rgb(253,211,43)", "Winter": "rgb(0,155,222)","Autumn": "rgb(171,68,1)","Spring": "rgb(151,189,25)"},
                labels=dict(depth_class='Classed depth below surface (m)'),
            )
            
        
        if len(input4)>0:
            fig.update_layout(
                yaxis = dict(autorange="reversed")
            )
        if len(input5)>1:
            fig.update_layout(
                xaxis = dict(autorange="reversed")
            )
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            font=dict(
                family="Times New Roman",
                    size=12
                
                ),
            
        )
#       fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        return fig
    except:
        raise PreventUpdate


    