import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import json

from ipywidgets import widgets
from dash.dependencies import Input, Output, State

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
visualization_list = ('Parcats', 'Heatmap', 'Stacked Bar Chart', 'Table')

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
    #html.Div([html.Pre(id='hover')], style={'width':'30%', 'float':'right'}),
    dcc.Tabs(children=[
        # Tab 1
        dcc.Tab(label='World Map', children=[
            html.Br(),
            dcc.Tabs(children=[
                dcc.Tab(label='Hot Spots', style=tab_style, selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(id='map_choropleth_1'),
                            # Graph 1
                            dcc.Graph(id='graph_1'),
                            # Graph 2
                            dcc.Graph(id='graph_2'),
                            dcc.Graph(id='graph_4')
                        ]),
                dcc.Tab(label='Deaths', style=tab_style, selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(id='map_bubble_1')
                        ]),
                dcc.Tab(label='Top Countries Distribution', style=tab_style, selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(id='graph_5'),
                            dcc.Graph(id='graph_6')
                        ]),
            ], style=tabs_styles),
        ]),
        # Tab 2
        dcc.Tab(label='Exploratory', children=[
            # row 1
            html.Div([
                html.Div([
                    html.H6('Country'),
                    dcc.Dropdown(
                        id='dropdown_country',
                        options=[{'label': i, 'value': i} for i in country_list],
                        multi=True,
                        value=['United States'],
                    )],
                    style={'width': '48%', 'display': 'inline-block'}),
            ]),
            # row 2
            html.Div([
                html.Div([
                    html.H6('Visualization'),
                    dcc.Dropdown(
                        id='dropdown_vis',
                        options=[{'label': i, 'value': i} for i in visualization_list],
                        value='Parcats',
                        clearable=False,
                    )],
                    style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    html.H6('Features'),
                    dcc.Dropdown(
                        id='dropdown_feature',
                        options=[{'label': i, 'value': i} for i in ['']],
                        multi=True,
                        value=[],
                        placeholder='Select data',
                    )],
                    style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ]),
            # row 3
            html.Br(),
            html.Div([
                dcc.RadioItems(
                    id='radio_count',
                    labelStyle={'display': 'inline-block'}
                ),
            ]),
            # row 4
            # visualization
            dcc.Store(id='memory_parcats'),
            dcc.Graph(id='expl_vis_parcats', style={'display': 'none'}),
            dcc.Graph(id='expl_vis_heatmap', style={'display': 'none'}),
            dcc.Graph(id='expl_vis_stacked', style={'display': 'none'}),
            dcc.Graph(id='expl_vis_table', style={'display': 'none'}),
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
                         lat='Lat', lon='Lon',
                         color_discrete_map={'crimson': 'crimson'},
                         size='Killed',
                         labels={'Lat': 'Latitude', 'Lon': 'Longitude'},
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
                             mode='lines+markers', name='# of Attacks'))
    fig.add_trace(go.Scatter(x=df_input['Year'], y=df_input['Killed'],
                             mode='lines+markers', name='# of Killed'))
    fig.add_trace(go.Scatter(x=df_input['Year'], y=df_input['Wounded'],
                             mode='lines+markers', name='# of Wounded'))

    # Edit the layout
    fig.update_layout(xaxis_title='Year', yaxis_title='Count')  # title='Terrorist attacks YoY',
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    return fig


def update_range_slider_text(min_year, max_year):
    return html.H3('Global Terrorist Attacks {}-{}'.format(min_year, max_year))


def update_graph_scatter(df_input):
    # Create traces
    fig = px.scatter(df_input, x='Year', y='Attack', size='Killed', color='Attack Type', size_max=40, opacity=0.4)
    return fig


def update_expl_vis_parcats(features, df_input):
    # print('Draw parcats')
    order = ['Country'] + [feature for feature in features]
    group_by = ['Region', 'Country', 'Attack Type', 'Weapon Type', 'Suicide', 'Success']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_tmp = df_input.groupby(group_by).agg(agg_on).reset_index()
    df_tmp.columns = ['Region','Country', 'Attack Type', 'Weapon Type', 'Suicide', 'Success',
                      'Attack', 'Killed', 'Wounded']
    dimensions = [dict(values=df_tmp[label], label=label) for label in order]

    # Build color scale
    parcats_length = len(df_tmp)
    color = np.zeros(parcats_length, dtype='uint8')
    colorscale = [[0, 'gray'], [1, 'firebrick']]

    # Build figure as FigureWidget
    fig = go.FigureWidget(
        data=[go.Scatter(x=df_tmp['Killed'],
                         y=df_tmp['Wounded'],
                         marker={'color': 'gray'},
                         mode='markers',
                         selected={'marker': {'color': 'firebrick'}},
                         unselected={'marker': {'opacity': 0.3}}),
              go.Parcats(domain={'y': [0, 0.4]},
                         dimensions=dimensions,
                         line={'colorscale': colorscale, 'cmin': 0, 'cmax': 1, 'color': color, 'shape': 'hspline'})
              ])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                      height=800, xaxis={'title': 'Killed'},
                      yaxis={'title': 'Wounded', 'domain': [0.6, 1]},
                      dragmode='lasso', hovermode='closest')
    return fig, len(df_tmp)


def update_expl_vis_heatmap(features, counts, df_input):
    # print('Draw heatmap')
    order = ['Country'] + [feature for feature in features]
    group_by = ['Country', 'City', 'Group', 'Attack Type', 'Target Type', 'Weapon Type', 'Suicide', 'Success']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_tmp = df_input.groupby(group_by).agg(agg_on).reset_index()
    df_tmp.columns = ['Country', 'City', 'Group', 'Attack Type', 'Target Type', 'Weapon Type', 'Suicide', 'Success',
                      'Attack', 'Killed', 'Wounded']
    fig = px.treemap(df_tmp, path=order, values=counts)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    return fig


def update_expl_vis_stacked(feature, counts, df_input):
    # print('Draw stacked')
    group_by = ['Country', feature]
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_tmp = df_input.groupby(group_by).agg(agg_on).reset_index()
    df_tmp.columns = ['Country', feature, 'Attack', 'Killed', 'Wounded']
    fig = px.bar(df_tmp, x='Country', y=counts, color=feature)  # title='Terorrist'
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    return fig


def update_expl_vis_table(features, df_input):
    # print('Draw table')
    order = ['Country', 'Date'] + [feature for feature in features]
    header = dict(values=order)
    cells = dict(values=[df_input[item] for item in order])
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    return fig


def display_hover_data(hover_data):
    country_name = hover_data['points'][0]['location']
    return json.dumps(country_name)


def get_box_plot_data(df_in, y_axis, top_n):
    df_box_year_country_all = df_in.groupby(['Country','Year']).agg({'eventid': ['size'], 
                                                                  'Killed':['sum']}).reset_index()

    df_box_year_country_all.columns = ['Country','Year', 'Attack', 'Killed']

    df_box_country_agg = df_box_year_country_all.groupby(['Country']).agg({y_axis: ['sum']}).reset_index()

    df_box_country_agg.columns = ['Country',y_axis]

    country_list = df_box_country_agg.sort_values(y_axis, ascending=False)['Country'][:top_n]

    df_box_country_filtered = df_box_year_country_all[df_box_year_country_all['Country'].isin(country_list)]
    
    return df_box_country_filtered


def get_weapon_type_data(df_in):
    df_weapon_type = df_in.groupby(['Year', 'Weapon Type']).agg({'eventid': ['size'],
	                                                      'Killed':['sum']}).reset_index()

    df_weapon_type.columns = ['Year', 'Weapon Type', 'Attack', 'Killed']
    df_weapon_type = df_weapon_type.replace(
        'Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)',
        'Vehicle')
        
    return df_weapon_type
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
    group_by = ['Country', 'Lat_round', 'Lon_round']
    agg_on = {'eventid': ['size'], 'Killed': ['sum'], 'Wounded': ['sum']}
    df_bubble = df_filtered.groupby(group_by).agg(agg_on).reset_index()
    df_bubble.columns = ['Country', 'Lat', 'Lon', 'Attack', 'Killed', 'Wounded']

    return update_map_choropleth_1(df_choropleth), \
           update_map_bubble_1(df_bubble), \
           update_range_slider_text(min_year, max_year)


@app.callback(
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    Output('graph_4', 'figure'),
    Input('year-range-slider', 'value'),
    Input('map_choropleth_1', 'hoverData')
    )
def update_graph_set_2(year_value, hover_data):
    if hover_data:
        dff = df[df['Country'] == hover_data['points'][0]['location']]
    else:
        dff = df
    
    min_year, max_year = year_value
    df_filtered = dff.query('Year>={}&Year<={}'.format(min_year, max_year))

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
    #Graph 4
    df_weapon_type = get_weapon_type_data(df_filtered)

    fig3 = px.scatter(df_weapon_type, x='Year', y='Attack', size='Killed', color='Weapon Type', 
	             size_max=40 , opacity = 0.4)
    return update_graph_line(df_kill_wound), \
           update_graph_scatter(df_year_attack), \
           fig3

@app.callback(
    Output('graph_5', 'figure'),
    Output('graph_6', 'figure'),
    Input('year-range-slider', 'value'),
    )
def update_graph_set_4(year_value):
    min_year, max_year = year_value
    df_filtered = df.query('Year>={}&Year<={}'.format(min_year, max_year))

    df_weapon_type = get_weapon_type_data(df_filtered)

    fig1 = px.scatter(df_weapon_type, x='Year', y='Attack', size='Killed', color='Weapon Type', 
	             size_max=40 , opacity = 0.3)
	             
    #-----------------------------------------------------------------------------------------             
    top_n = 10
    y_axis = 'Killed'#'Attack'

    df_box_country_filtered = get_box_plot_data(df, y_axis, top_n)
    fig2 = px.violin(df_box_country_filtered, x='Country',y=y_axis)

    top_n = 10
    y_axis = 'Attack'#'Attack'
    df_box_country_filtered = get_box_plot_data(df, y_axis, top_n)
    fig3 = px.violin(df_box_country_filtered, x='Country',y=y_axis)
    
    return fig2, fig3

@app.callback(
    Output('dropdown_feature', 'multi'),
    Output('dropdown_feature', 'options'),
    Output('dropdown_feature', 'value'),
    Output('radio_count', 'options'),
    Output('radio_count', 'value'),
    Input('dropdown_vis', 'value'),
    )
def update_selections(vis):
    feature_multi = None
    feature_options = list()
    feature_value = list()
    count_options = list()
    count_value = ''
    if vis.lower() == 'parcats':
        feature_multi = True
        feature_options = [{'label': i, 'value': i} for i in ['Attack Type', 'Weapon Type', 'Region',
                                                              'Suicide', 'Success']]
        feature_value = ['Attack Type', 'Weapon Type']
    elif vis.lower() == 'heatmap':
        feature_multi = True
        feature_options = [{'label': i, 'value': i} for i in ['City', 'Group', 'Attack Type', 'Target Type',
                                                              'Weapon Type', 'Suicide', 'Success']]
        feature_value = ['Attack Type', 'Weapon Type']
        count_options = [{'label': i, 'value': i} for i in ['Attack', 'Killed', 'Wounded']]
        count_value = 'Killed'
    elif vis.lower() == 'stacked bar chart':
        feature_multi = False
        feature_options = [{'label': i, 'value': i} for i in ['City', 'Group', 'Attack Type', 'Target Type',
                                                              'Weapon Type', 'Suicide', 'Success']]
        feature_value = 'Attack Type'
        count_options = [{'label': i, 'value': i} for i in ['Attack', 'Killed', 'Wounded']]
        count_value = 'Killed'
    elif vis.lower() == 'table':
        feature_multi = True
        feature_options = [{'label': i, 'value': i} for i in ['Region', 'City', 'Group', 'Attack Type', 'Target Type',
                                                              'Weapon Type', 'Suicide', 'Success', 'Killed', 'Wounded',
                                                              'Summary', 'Target', 'Nationality', 'Motive']]
        feature_value = ['Region', 'City']
    return feature_multi, feature_options, feature_value, count_options, count_value


@app.callback(
    Output('expl_vis_parcats', 'figure'),
    Output('memory_parcats', 'data'),
    Output('expl_vis_parcats', 'style'),
    Input('year-range-slider', 'value'),
    Input('dropdown_country', 'value'),
    Input('dropdown_vis', 'value'),
    Input('dropdown_feature', 'value'),
    Input('expl_vis_parcats', 'selectedData'),
    Input('expl_vis_parcats', 'clickData'),
    State('expl_vis_parcats', 'figure'),
    State('memory_parcats', 'data')
)
def update_vis_parcats(year_value, countries, vis, features, selected_data, click_data, fig, data):
    if vis.lower() != 'parcats':
        return dash.no_update, dash.no_update, {'display': 'none'}
    elif not countries or not features:
        return dash.no_update, dash.no_update, dash.no_update
    elif any([True for item in dash.callback_context.triggered
              if item['prop_id'] in ('year-range-slider.value', 'dropdown_country.value', 'dropdown_feature.value')]):
        min_year, max_year = year_value
        country_filter = ['Country=="{}"'.format(country) for country in countries]
        df_filtered = df.query('Year>={}&Year<={}&({})'.format(min_year, max_year, '|'.join(country_filter)))
        return *update_expl_vis_parcats(features, df_filtered), {'display': 'block'}
    else:
        selection = None
        # Update selection based on which event triggered the update.
        trigger = dash.callback_context.triggered[0]['prop_id']
        if trigger == 'expl_vis_parcats.clickData':
            selection = [point['pointNumber'] for point in click_data['points']]
        if trigger == 'expl_vis_parcats.selectedData':
            selection = [point['pointIndex'] for point in selected_data['points']]
        # Update scatter selection
        fig['data'][0]['selectedpoints'] = selection
        # Update parcats colors
        new_color = np.zeros(data, dtype='uint8')
        new_color[selection] = 1
        fig['data'][1]['line']['color'] = new_color
        return fig, dash.no_update, {'display': 'block'}


@app.callback(
    Output('expl_vis_heatmap', 'figure'),
    Output('expl_vis_heatmap', 'style'),
    Input('year-range-slider', 'value'),
    Input('dropdown_country', 'value'),
    Input('dropdown_vis', 'value'),
    Input('dropdown_feature', 'value'),
    Input('radio_count', 'value'),
)
def update_vis_heatmap(year_value, countries, vis, features, counts):
    if vis.lower() != 'heatmap':
        return dash.no_update, {'display': 'none'}
    elif not countries or not features:
        return dash.no_update, dash.no_update
    else:
        min_year, max_year = year_value
        country_filter = ['Country=="{}"'.format(country) for country in countries]
        df_filtered = df.query('Year>={}&Year<={}&({})'.format(min_year, max_year, '|'.join(country_filter)))
        return update_expl_vis_heatmap(features, counts, df_filtered), {'display': 'block'}


@app.callback(
    Output('expl_vis_stacked', 'figure'),
    Output('expl_vis_stacked', 'style'),
    Input('year-range-slider', 'value'),
    Input('dropdown_country', 'value'),
    Input('dropdown_vis', 'value'),
    Input('dropdown_feature', 'value'),
    Input('radio_count', 'value'),
)
def update_vis_stacked(year_value, countries, vis, features, counts):
    if vis.lower() != 'stacked bar chart':
        return dash.no_update, {'display': 'none'}
    elif not countries or not features:
        return dash.no_update, dash.no_update
    else:
        min_year, max_year = year_value
        country_filter = ['Country=="{}"'.format(country) for country in countries]
        df_filtered = df.query('Year>={}&Year<={}&({})'.format(min_year, max_year, '|'.join(country_filter)))
        return update_expl_vis_stacked(features, counts, df_filtered), {'display': 'block'}


@app.callback(
    Output('expl_vis_table', 'figure'),
    Output('expl_vis_table', 'style'),
    Input('year-range-slider', 'value'),
    Input('dropdown_country', 'value'),
    Input('dropdown_vis', 'value'),
    Input('dropdown_feature', 'value'),
)
def update_vis_table(year_value, countries, vis, features):
    if vis.lower() != 'table':
        return dash.no_update, {'display': 'none'}
    elif not countries or not features:
        return dash.no_update, dash.no_update
    else:
        min_year, max_year = year_value
        country_filter = ['Country=="{}"'.format(country) for country in countries]
        df_filtered = df.query('Year>={}&Year<={}&({})'.format(min_year, max_year, '|'.join(country_filter)))
        return update_expl_vis_table(features, df_filtered), {'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=False)
