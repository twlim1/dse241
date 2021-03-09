import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

tabs_styles = {
    'height': '35px',
    'width': '40%',
    'margin-left': '30%',
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

# Reading the data
df = pd.read_csv(r'data/all.csv')
country_list = df['Country'].sort_values().unique()
year_max = df['Year'].max()
year_min = df['Year'].min()

# Basic Stats 
print('Dataframe shape: {}'.format(df.shape))
print('Attacks between: {} - {}'.format(year_min, year_max))

app.layout = html.Div([
    # DatePickerRange
    html.Center(
        html.Div(id='slider-text', children=[html.H3('Global Terrorist Attacks {}-{}'.format(year_min, year_max))])
    ),
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
        dcc.Tab(label='World Map', children=[
            html.Br(),
            dcc.Tabs(children=[
                dcc.Tab(label='Hot Spots', style=tab_style, selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(id='map_choropleth_1')
                        ]),
                dcc.Tab(label='Deaths', style=tab_style, selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(id='map_bubble_1')
                        ]),
                # dcc.Tab(label='Injuries', style=tab_style, selected_style=tab_selected_style)
            ], style=tabs_styles)
        ]),
        # Tab 2
        dcc.Tab(label='Dashboard', children=[
            # Graph 1
            dcc.Graph(id='graph_1'),
            # Graph 2
            dcc.Graph(id='graph_2')
        ]),
        # Tab 3
        dcc.Tab(label='Exploratory', children=[
            html.Div([
                html.Div([
                    html.H6('Country'),
                    dcc.Dropdown(
                        id='dropdown_1',
                        options=[{'label': i, 'value': i} for i in country_list],
                        value='United States'
                        # value='Iraq'
                    )],
                    style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    html.H6('Data'),
                    dcc.Dropdown(
                        id='dropdown_2',
                        options=[{'label': i, 'value': i} for i in ('Attack Type', 'City', 'Weapon Type')],
                        multi=True,
                        value=['City']
                    )],
                    style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ]),
            dcc.RadioItems(
                id='map_type',
                options=[{'label': i, 'value': i} for i in ['Both', 'Killed', 'Injured']],
                value='Choropleth',
                labelStyle={'display': 'inline-block'}
            ),
            # Graph 3
            dcc.Graph(id='graph_3')
        ])
    ])
])


def update_map_choropleth_1(df_input):
    fig = px.choropleth(df_input,
                        locations='Country',
                        locationmode='country names',
                        color='Attack',
                        range_color=(0, 4000),
                        hover_name='Country',
                        projection='natural earth',  # 'orthographic',
                        color_continuous_scale='YlOrRd')
    fig.update_layout(margin={'r': 0, 't': 20, 'l': 0, 'b': 0},
                      geo=dict(landcolor='rgb(250, 250, 250)'))
    return fig


def update_map_bubble_1(df_input):
    kill_no = 5
    fig = px.scatter_geo(df_input[df_input['Killed'] > kill_no],
                         lat='lat', lon='lon',
                         color_discrete_map={'crimson': 'crimson'},
                         size='Killed',
                         labels={'lat': 'Latitude', 'lon': 'Longitude'},
                         hover_name='Country',
                         projection='natural earth',  # 'orthographic',
                         size_max=40)
    fig.update_layout(margin={'r': 0, 't': 20, 'l': 0, 'b': 0},
                      geo=dict(landcolor='rgb(250, 250, 250)'))
    return fig


def update_graph_line(df_input):
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_input['Year'], y=df_input['Attacks'],
                             mode='lines+markers', name='Attacks'))
    fig.add_trace(go.Scatter(x=df_input['Year'], y=df_input['Killed'],
                             mode='lines+markers', name='Killed'))
    fig.add_trace(go.Scatter(x=df_input['Year'], y=df_input['Wounded'],
                             mode='lines+markers', name='Wounded'))

    # Edit the layout
    fig.update_layout(xaxis_title='Year', yaxis_title='Count')  # title='Terrorist attacks YoY',
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    return fig


def update_range_slider_text(min_year, max_year):
    return html.H3('Global Terrorist Attacks {}-{}'.format(min_year, max_year))


def update_graph_scatter(df_input):
    # Create traces
    fig = px.scatter(df_input, x='Year', y='Attack', size='Killed', color='Attack Type', size_max=40)
    return fig


def update_graph_treemap(df_input, selections):
    # Create traces
    order = ['Country']
    if selections:
        for i in selections:
            order.append(i)
    # print('here')
    # print(order)
    fig = px.treemap(df_input, path=order, values='Killed')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    return fig


@app.callback(
    Output('map_choropleth_1', 'figure'),
    Output('map_bubble_1', 'figure'),
    Output('slider-text', 'children'),
    Input('year-range-slider', 'value')
    )
def update_graph_set_1(year_value):
    min_year, max_year = year_value
    df_filtered = df.query('Year>={}&Year<={}'.format(min_year, max_year))

    # Map Choropleth
    group_by = ['Country']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_choropleth = df_filtered.groupby(group_by).agg(agg_on).reset_index()
    df_choropleth.columns = ['Country', 'Attack', 'Killed', 'Wounded']

    # Map Bubble
    group_by = ['Country', 'lat_round', 'lon_round']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_bubble = df_filtered.groupby(group_by).agg(agg_on).reset_index()
    df_bubble.columns = ['Country', 'lat', 'lon', 'Attack', 'Killed', 'Wounded']

    return update_map_choropleth_1(df_choropleth), \
           update_map_bubble_1(df_bubble), \
           update_range_slider_text(min_year, max_year)


@app.callback(
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    Input('year-range-slider', 'value')
    )
def update_graph_set_2(year_value):
    min_year, max_year = year_value
    df_filtered = df.query('Year>={}&Year<={}'.format(min_year, max_year))

    # Graph 1
    group_by = ['Year']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_kill_wound = df_filtered.groupby(group_by).agg(agg_on).reset_index()
    df_kill_wound.columns = ['Year', 'Attacks', 'Killed', 'Wounded']

    # Graph 2
    group_by = ['Year', 'Attack Type']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_year_attack = df_filtered.groupby(group_by).agg(agg_on).reset_index()
    df_year_attack.columns = ['Year', 'Attack Type', 'Attack', 'Killed', 'Wounded']

    return update_graph_line(df_kill_wound), \
           update_graph_scatter(df_year_attack)


@app.callback(
    Output('graph_3', 'figure'),
    Input('year-range-slider', 'value'),
    Input('dropdown_1', 'value'),
    Input('dropdown_2', 'value')
    )
def update_graph_set_3(year_value, country, selections):
    min_year, max_year = year_value
    df_filtered = df.query('Year>={}&Year<={}'.format(min_year, max_year))

    # Graph 3
    group_by = ['Year', 'Region', 'Country', 'City', 'Attack Type', 'Weapon Type']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_country_attack = df_filtered.groupby(group_by).agg(agg_on).reset_index()
    df_country_attack.columns = ['Year', 'Region', 'Country', 'City', 'Attack Type', 'Weapon Type', 'Attack', 'Killed', 'Wounded']
    df_country_attack = df_country_attack.query('Country=="{}"'.format(country))

    return update_graph_treemap(df_country_attack, selections)


if __name__ == '__main__':
    app.run_server(debug=True)
