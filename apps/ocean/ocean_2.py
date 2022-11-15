#!/Users/privateprivate/envs/bin/python

import os
from dash.exceptions import PreventUpdate
import dash
from dash import html, dcc, Output, Input
import dash_leaflet as dl
from dash_extensions.javascript import assign

from app import app


def dicts_to_geojson(dicts, lat="lat", lon="lon"):
	geojson = {"type": "FeatureCollection", "features": []}
	for d in dicts:
		feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [d[lon], d[lat]]}}
		props = [key for key in d.keys() if key not in [lat, lon]]
		if props:
			feature["properties"] = {prop: d[prop] for prop in props}
		geojson["features"].append(feature)
	return geojson
## Cool, dark tiles by Stadia Maps.
style = {'width': '49%', 'height': '500px', 'float': 'left'}
style2 = {'width': '49%', 'height': '500px', 'float': 'right'}
## Cool, dark tiles by Stadia Maps.
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




# A few cities in Denmark.
cities = [dict(name="PELTERP1", lat=-33.89616667, lon=25.70227778),
	dict(name="PELTERP2", lat=-33.82624, lon=25.75429),
	dict(name="PELTERP3", lat=-33.76805556, lon=25.90602778),
	dict(name="PELTERP4", lat=-33.73205556, lon=26.06397222),
	dict(name="PELTERP5", lat=-33.75666667, lon=26.23477778),
	dict(name="PELTERP6", lat=-33.86869, lon=26.2914599999999),
	dict(name="PELTERP7", lat=-33.88177, lon=25.98722),
	dict(name="PELTERP8", lat=-34.034167, lon=25.727778)]
# Generate geojson with a marker for each city and name as tooltip.
geojson = dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in cities])
# Create javascript function that filters out all cities but Aarhus.
geojson_filter = assign("function(feature, context){{return ['PELTERP1'].includes(feature.properties.name);}}")


point_to_layer = assign("""function(feature, latlng, context){
		// Figure out if the marker is selected.
		//const selected = context.props.hideout.includes(feature.properties.name);
		// Render selected markers in red.
		//if(selected){return L.circleMarker(latlng, {color: 'red'});}
		// Render non-selected markers in blue.
		//circleOptions.fillColor = 'red'
		return L.circleMarker(latlng, {fillColor: 'red', fillOpacity: '0.75',Opacity: '1'});
}""")

layout = html.Div([dl.Map([
	dl.LayersControl([
		dl.BaseLayer(dl.TileLayer(url=CartoDB_Positron,attribution=attribution_CartoDB_Positron,),
			name="CartoDB.Positron",
			checked="CartoDB.Positron" == "CartoDB.Positron",)]
		+ [dl.BaseLayer(dl.TileLayer(url=googleUrl, attribution=googleUrlattribution),
			name="Google Sat",)]
		+ [dl.BaseLayer(dl.TileLayer(url=esriUrl, attribution=esriUrlattribution),name="Esri",)]
		+ [dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_50cm_MOSAIC",layers="CDNGI_Imagery_50cm_MOSAIC",format="image/png",transparent=True,)),name="CDNGI_Imagery_50cm_MOSAIC",)]
		+ [dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_25cm_MOSAIC_2017",layers="CDNGI_Imagery_25cm_MOSAIC_2017",format="image/png",transparent=True,)),name="CDNGI_Imagery_25cm_MOSAIC_2017",)]
		+ [dl.Overlay(dl.LayerGroup(dl.WMSTileLayer(url="http://apollo.cdngiportal.co.za/erdas-iws/ogc/wms/CDNGI_Imagery_25cm_MOSAIC_2018",layers="CDNGI_Imagery_25cm_MOSAIC_2018",format="image/png",transparent=True,)),name="CDNGI_Imagery_25cm_MOSAIC_2018",)]), dl.GeoJSON(data=geojson,  cluster=True,zoomToBoundsOnClick=True,options=dict(pointToLayer=point_to_layer),id="geojson"),
	
	#   dl.GestureHandling()
],
	zoom=9,
	center=(-33.681, 25.842),
	style=style,
	id="map",
),
	html.Div(
		id="capital")
])

@app.callback(Output("capital", "children"), Input("geojson", "click_feature"))
def capital_click(feature):
	triggered = dash.callback_context.triggered
	#   print(triggered[0]['value']['properties']['name'])
#	if(triggered[0]['value']['properties']['cluster']):
#		raise PreventUpdate
#		return
	try:
		#       if feature is not None:
		if triggered[0]['value']['properties']['name'] == 'PELTERP1':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP1",
	style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP2':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP2",
		style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP3':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP3",
		style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP4':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP4",
		style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP5':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP5",
		style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP6':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP6",
		style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP7':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP7",
		style=style2)
		elif triggered[0]['value']['properties']['name'] == 'PELTERP8':
			return html.Iframe(src="https://dash.saeon.ac.za/apps/ocean/PELTERP8",
		style=style2)
		else:
			return
	except:
		return
	