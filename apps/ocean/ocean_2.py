#!/Users/privateprivate/envs/bin/python

import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
#from dash import Dash, html
#import random  
#import dash  
#import dash_leaflet.express as dlx  
#from dash_extensions.javascript import Namespace
#from dash_extensions.javascript import assign
#from dash_extensions.javascript import arrow_function
#import os
#assets_path = os.getcwd() +'/assets'
#print(os.getcwd())
from app import app

## Cool, dark tiles by Stadia Maps.
url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '


osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
osmUrlattribution = '<a href="http://openstreetmap.org">OpenStreetMap</a>'

googleUrl= 'http://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
googleUrlattribution = 'google'

esriUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
esriUrlattribution = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'

Stadia_AlidadeSmooth = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
attribution_Stadia_AlidadeSmooth = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'

CartoDB_Positron = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'
attribution_CartoDB_Positron = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'

layout = html.Div([dl.Map([
	dl.LayersControl(
		[dl.BaseLayer(dl.TileLayer(url=CartoDB_Positron, attribution=attribution_CartoDB_Positron),
			name="CartoDB.Positron", checked= "CartoDB.Positron"=="CartoDB.Positron")]+									
		[dl.BaseLayer(dl.TileLayer(url=googleUrl, attribution=googleUrlattribution),
			name="Google Sat")]+									
		[dl.BaseLayer(dl.TileLayer(url=esriUrl, attribution=esriUrlattribution),
			name="Esri")]+
		[dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_50cm_MOSAIC",
			layers="CDNGI_Imagery_50cm_MOSAIC", format="image/png", transparent=True)), name="CDNGI_Imagery_50cm_MOSAIC")]+
		[dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url='http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_25cm_MOSAIC_2017',layers="CDNGI_Imagery_25cm_MOSAIC_2017", format="image/png", transparent=True)), name="CDNGI_Imagery_25cm_MOSAIC_2017")]+
		[dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url='http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_25cm_MOSAIC_2018',
			layers="CDNGI_Imagery_25cm_MOSAIC_2018", format="image/png", transparent=True)), name="CDNGI_Imagery_25cm_MOSAIC_2018")]
		#       [dl.TileLayer(),dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
		#           activeColor="#214097", completedColor="#972158")]
	)
	
	#, dl.GestureHandling()
],  zoom=5, center=(-30, 27), style={'width': '75%', 'height': '75vh', 'margin': "auto", "display": "block",'margin-left': '0px'},   id="map"),
	html.Div(id="Marc_state")
	
])
