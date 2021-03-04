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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
    html.Div(id='slider-text', children=[
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
            html.Br(),
            html.Iframe(id='map_1', srcDoc=open('Excercise7-markers-Groups.html', 'r').read(),width='100%', height='700')
        ]),
        # Tab 2
        dcc.Tab(label='HeatMap', children=[
            # DatePickerRange
            html.Br(),
            html.Iframe(id='map_2', srcDoc=open('Excercise7-Heatmap.html', 'r').read(),width='100%', height='700')
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
    #updating map_1
    # create empty map zoomed in on California by cluster grouping.
    map_1 = folium.Map(location=CA_COORDINATES,tiles="OpenStreetMap", zoom_start=6)
    for idx in range(dff.shape[0]):
        county = dff['County'].iloc[idx]
        cases = dff['Positive_Cases'].iloc[idx]
        week = dff['Week_Reported'].iloc[idx]
        year = dff['Year'].iloc[idx]
    g = folium.FeatureGroup(name='West Nile Virus Cases')
    g.add_child(MarkerCluster(locations=dffmapdata))
    g.add_child(folium.Popup("County:{}\n Cases:{}\n Week:{}\n Year:{}".format(county,cases,week, year)))
    map_1.add_child(g)
    folium.TileLayer('Stamen Terrain').add_to(map_1)
    folium.TileLayer('Stamen Toner').add_to(map_1)
    folium.TileLayer('Stamen Water Color').add_to(map_1)
    folium.TileLayer('cartodbpositron').add_to(map_1)
    folium.TileLayer('cartodbdark_matter').add_to(map_1)
    folium.LayerControl().add_to(map_1)
    map_1.save('Excercise7-markers-Groups.html')
    
    map2 = folium.Map(location=CA_COORDINATES,tiles='OpenStreetMap', zoom_start=6)
    HeatMap(dffmapdata).add_to(map2)
    map2.save('Excercise7-Heatmap.html')
    return open('Excercise7-markers-Groups.html', 'r').read()

@app.callback(
    Output('map_2', 'srcDoc'),
    Input('year-range-slider', 'value')
    )
    
def update_map2(year_value):
    min_year, max_year = year_value
    #return('You have selected "{}"').format(year_value)
    #update map based on range filter
    dff=[]
    dff= df.query('Year>={}&Year<={}'.format(min_year, max_year))
    dffmapdata=dff[['Longitude', 'Latitude']].values.tolist()
    #updating map_1
    map2 = folium.Map(location=CA_COORDINATES,tiles='OpenStreetMap', zoom_start=6)
    HeatMap(dffmapdata).add_to(map2)
    map2.save('Excercise7-Heatmap.html')
    return open('Excercise7-HeatMap.html', 'r').read()

if __name__ == '__main__':
    app.run_server(debug=True)
