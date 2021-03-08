import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import folium
from ipywidgets import interact
from ipywidgets import interact
from dash.dependencies import Input, Output
import os
import folium
import geocoder
from folium.plugins import HeatMap, HeatMapWithTime
from folium.plugins import MarkerCluster
from folium import IFrame
from folium import Marker
import base64
import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['assets/bWLwgP.css']

tabs_styles = {
    'height': '40px',
    'width': '48%',
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Reading the data and doing basic formating..
df = pd.read_csv("West_Nile_Virus_by_County.csv")
df['formatted_date'] = df['Year'] * 1000 + df['Week_Reported'] * 10 + 0
df['date'] = pd.to_datetime(df['formatted_date'], format='%Y%W%w')
counties=df["County"].unique()
g = geocoder.osm(str(df['County'][0])+" County, CA")
g.geojson['features'][0]['geometry']['coordinates']
geocounties=[]
for x in counties:
    geocounties.append(geocoder.osm(str(x)+" County, CA").geojson['features'][0]['geometry']['coordinates'])
countiesdf=pd.DataFrame()
countiesdf['geoLocation']=geocounties
countiesdf=pd.DataFrame(countiesdf['geoLocation'].to_list(), columns=['Latitude','Longitude'])
countiesdf['County']=counties
countiesdf.head()
df=df.merge(countiesdf)
df=df.sort_values(["date"])
dfmapdata=df[["Longitude", "Latitude"]].values.tolist()
#tuple(dfmapdata[0])

CA_COORDINATES = (36.7783, -119.4179)

# Basic Stats 
counties_list = df['County'].sort_values().unique()
year_max = df['Year'].max()
year_min = df['Year'].min()

# Basic Stats 
print('Dataframe shape: {}'.format(df.shape))
print('Virus cases between: {} - {}'.format(df['Year'].min(), df['Year'].max()))

app.layout = html.Div([
    # DatePickerRange
    html.Div(id='slider-text',children=[
        html.H3('West Nile Virus Spread {}-{}'.format(year_min, year_max))]),
        dcc.RangeSlider(
            id='year-range-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=[df['Year'].min(), df['Year'].max()],
            marks={str(year): ('' if year % 2 else str(year)) for year in df['Year'].unique()},
            step=1
        ),
        dcc.Tabs(children=[
        # Tab 1
        
        dcc.Tab(label='MarkerCluster', children=[
            # DatePickerRange
            html.Img(src=app.get_asset_url('my-image.png'), style={'height':'20%', 'width':'300px','position': 'absolute','bottom': '30px','left': '15px','right': '15px','width': '300px'}),
            html.Br(),
            html.Iframe(id='map_1', srcDoc=open('Excercise7-markers-Groups.html', 'r').read(),width='100%', height='700')
        ])
    ])
])
     
@app.callback(
    Output('map_1', 'srcDoc'),
    Input('year-range-slider', 'value')
    )
  
def update_map1(year_value):
    min_year, max_year = year_value
    #return('You have selected "{}"').format(year_value)
    #update map based on range filter
    dff=[]
    dff= df.query('Year>={}&Year<={}'.format(min_year, max_year))
    dffmapdata=dff[['Longitude', 'Latitude']].values.tolist()
    res_popups=[]
    for idx in range(dff.shape[0]):
        test = folium.Html('<b>Hello world</b>', script=True)
        county = dff['County'].iloc[idx]
        cases = dff['Positive_Cases'].iloc[idx]
        week = dff['Week_Reported'].iloc[idx]
        year = dff['Year'].iloc[idx]
        res_popups.append("County:{}\n Cases:{}\n Week:{}\n Year:{}".format(county,cases,week, year))
    #updating map_1
    # create empty map zoomed in on California by cluster grouping.
    map_1 = folium.Map(location=CA_COORDINATES,tiles="OpenStreetMap", zoom_start=6)
    g = folium.FeatureGroup(name='West Nile Virus Cases')
    g.add_child(MarkerCluster(locations=dffmapdata,popups=res_popups))
    map_1.add_child(g)
    folium.TileLayer('Stamen Terrain').add_to(map_1)
    folium.TileLayer('Stamen Toner').add_to(map_1)
    folium.TileLayer('Stamen Water Color').add_to(map_1)
    folium.TileLayer('cartodbpositron').add_to(map_1)
    folium.TileLayer('cartodbdark_matter').add_to(map_1)
    folium.LayerControl().add_to(map_1)
    map_1.save('Excercise7-markers-Groups.html')
    filename = "Excercise7-markers-Groups.html"
    with open(filename, 'r+') as f:
        text = f.read()
        text = re.sub("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css", 'assets/MarkerCluster.Default.css', text)
        f.seek(0)
        f.write(text)
        f.truncate()
    
    return open('Excercise7-markers-Groups.html', 'r').read()


if __name__ == '__main__':
    app.run_server(debug=True)
