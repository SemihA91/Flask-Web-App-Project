import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
from .classes.map import Map
import plotly.graph_objects as go


df_meteor = pd.read_csv("dash_app2/data/meteor_countries.csv")
df_volcano = pd.read_csv("dash_app2/data/volcano_data2.csv")
df_meteor['Type'] = 'meteorite'
df_volcano['Type'] = 'volcano'


# Create instance of map
map = Map(df_meteor, df_volcano)


def make_indicator(value, data_type, dark_mode):
    """
    Create the side bar indicator when points on the map
    are hovered over

    Parameters
    ----------
    value : int
        Meteor mass
    data_type : String
        Indicates if data is volcano or meteor
    dark_mode : Boolean
        Selects if dark mode is dislpayed

    Returns
    -------
    fig : .Graph
        The generated indicator

    """
    if data_type == 'volcano':
        title = {'text': "Volcanic Explosivity Index"}
        data_range = (0, 8)
        color = 'red'
        tick = 1
    else:
        title = {'text': "Meteor Mass (kg)"}
        data_range = (0, 1000)
        color = 'orange'
        value = value / 1000
        tick = 100

    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        gauge={
            'shape': 'angular',
            'bar': {'color': color},
            'axis': {'range': data_range, 'dtick': tick, 'tickangle': 0}
        },
        value=value,
        title=title
    ))

    fig.update_layout(
        height=300,
        font={'size': 15, 'color': ('white' if dark_mode else 'black')},
        margin={'l': 60, 'r': 60, 't': 0, 'b': 0},
        paper_bgcolor=('#282828' if dark_mode else 'white')
    )

    return fig


def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard",
                         url_base_pathname="/dash/", assets_folder='assets')
    dash_app.config.suppress_callback_exceptions = True
    dash_app.layout = html.Div(
        className="container",
        id="tab-layout",
        children=[
            html.Div([
                dcc.Store(id='dark-mode'),
                html.Div(
                    children=[
                        html.Div(
                            className="app-header",
                            children=[
                                html.Div(className="container", children=[
                                    html.Img(
                                        src=dash_app.get_asset_url(
                                            'logo_square.png'),
                                        height="80"
                                    ),
                                    html.H1(
                                        'INTERNATIONAL GEOGRAPHIC',
                                        className="title"
                                    )
                                ]),
                            ]
                        ),
                        html.Div(children=[
                            dbc.Button(dbc.Nav(dbc.NavLink('Return to Home',
                                       href="/", active=True,
                                       external_link=True, style={
                                           'textDecoration': 'none'}))),
                        ], style={'display': 'inline-block',
                                  'position': 'relative',
                                  'bottom': '90px',
                                  'left': '50px'}

                        ),
                    ],
                ),
            ]),

            html.Div(className="map-header", children=[

                html.Div(className='button-menu', children=[
                    'Select points to show: ',
                    dcc.Checklist(
                        className="radio-buttons",
                        id='select-traces',
                        options=[{'label': 'Meteorites',
                                  'value': 'Meteorites'}, {
                            'label': 'Volcanoes', 'value': 'Volcanoes'}],
                        value=[
                            'Meteorites', 'Volcanoes']
                    )
                ], style={'margin-left': '0%'}),
                # Toggle year colours
                html.Div(className="year-colours-button", children=[
                    daq.ToggleSwitch(
                        id='toggle-year-colours',
                        label='Show Year as Colour',
                        value=False,
                        size=40,
                        color='orange'
                    )
                ], style={'display': 'inline-block'}),
                # Toggle 2D/3D mode
                html.Div(className="mode-3D", children=[
                    daq.ToggleSwitch(
                        id='toggle-map-mode',
                        label='3D Mode 🌎',
                        value=False,
                        size=40,
                        color='orange'
                    )
                ], style={'display': 'inline-block', 'float': 'right'}),
            ], style={'margin-right': '40%'}),

            html.Div([
                html.Div(
                    children=[html.Div(id="map")],
                    style={
                        'width': '65%',
                        'display': 'inline-block',
                        'float': 'left',
                        'backgroundColor': 'white'
                    },
                    className='card'
                ),
                html.Div(
                    children=[html.Div(id="info")],
                    style={
                        'width': '27%',
                        'display': 'inline-block',
                        'float': 'right',
                        'backgroundColor': 'white',
                        'margin-right': '20px'

                    },
                    className='card'
                )
            ], style={'display': 'block', 'height': '550px'}),

            html.Br(), html.Br(),

            # Sliders
            html.Div([
                html.Div([
                    html.Div([
                        html.P('Meteor dates')
                    ], style={
                        'width': '8%',
                        'display': 'inline-block',
                        'float': 'left',
                        'padding-left': '20px'
                    }),

                    html.Div([
                        dcc.RangeSlider(
                            id='meteor-year-slider',
                            min=1950,
                            max=df_meteor['year'].max(),
                            marks={
                                1950: {'label': '1950',
                                       'style': {'color': '#77b0b1'}},
                                1980: {'label': '1980'},
                                2000: {'label': '2000'},
                                2020: {'label': '2020',
                                       'style': {'color': '#77b0b1'}}
                            },
                            tooltip={"placement": "bottom",
                                     "always_visible": True},
                            step=1,
                            allowCross=False,
                            value=[1960, 1980],
                        ),
                    ], style={
                        'width': '90%',
                        'display': 'inline-block',
                        'float': 'right'
                    }),
                ], style={'display': 'block'}),

                html.Br(), html.Br(), html.Br(),

                html.Div([
                    html.Div([
                        html.P('Volcano dates')
                    ], style={
                        'width': '8%',
                        'display': 'inline-block',
                        'float': 'left',
                        'margin': '-10px 0px 0px 20px'
                    }),

                    html.Div([
                        dcc.RangeSlider(
                            id='volcano-year-slider',
                            min=1950,
                            max=df_volcano['year'].max(
                            ),
                            marks={
                                1950: {'label': '1950',
                                       'style': {'color': '#77b0b1'}},
                                1980: {'label': '1980'},
                                2000: {'label': '2000'},
                                2020: {'label': '2020',
                                       'style': {'color': '#77b0b1'}}
                            },
                            tooltip={"placement": "bottom",
                                     "always_visible": True},
                            step=1,
                            allowCross=False,
                            value=[1960, 1980]
                        )
                    ], style={
                        'width': '90%',
                        'display': 'inline-block',
                        'float': 'right'
                    }),
                ], style={'display': 'block'}),
            ])])

    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(app):
    @ app.callback(
        Output('map', 'children'),
        [Input('toggle-map-mode', 'value'),
            Input('select-traces', 'value'),
            Input('meteor-year-slider', 'value'),
            Input('volcano-year-slider', 'value'),
            Input('toggle-year-colours', 'value')],
        State('dark-mode', 'data')
    )
    def update_map(map_mode, traces, meteor_year_range, volcano_year_range,
                   year_colour, dark_mode):
        df_meteor_filtered = df_meteor[df_meteor.year >= meteor_year_range[0]]
        df_meteor_filtered = df_meteor_filtered[
            df_meteor_filtered.year <= meteor_year_range[1]]
        df_volcano_filtered = df_volcano[
            df_volcano.year >= volcano_year_range[0]]
        df_volcano_filtered = df_volcano_filtered[
            df_volcano_filtered.year <= volcano_year_range[1]]
        map.set_dark_mode(dark_mode)
        map.update_dataframes(df_meteor_filtered, df_volcano_filtered)
        map.set_year_colours(year_colour)
        map.set_mode_3d(map_mode)
        map.set_show_meteor('Meteorites' in traces)
        map.set_show_volcano('Volcanoes' in traces)
        return dcc.Graph(id='map-graph', figure=map.get_fig())

    @ app.callback(
        Output('info', 'children'),
        Input('map-graph', 'hoverData'),
        State('dark-mode', 'data')
    )
    def update_info(hoverData, dark_mode):
        default_message = '''Move your cursor over a datapoint
                            to find out more about it!'''

        if hoverData is None:
            return html.H4(default_message)

        point_data = hoverData['points'][0]['customdata']

        contents = [
            html.H1(str(point_data[1])),
            html.P("Latitude: {}, Longitude: {}".format(
                point_data[2], point_data[3]))
        ]

        if point_data[0] == "meteorite":
            contents.append(html.P("Country: {}".format(point_data[6])))
            contents.append(html.P("Mass: {} g".format(point_data[5])))
            contents.append(html.P("Year: {} ({})".format(point_data[7],
                                                          point_data[9])))
            contents.append(html.P("Class: {}".format(point_data[8])))
            contents.append(dcc.Graph(
                figure=make_indicator(point_data[5], 'meteorite', dark_mode)))

        if point_data[0] == "volcano":
            contents.append(html.P("Erruption Date: {}".format(point_data[6])))
            contents.append(html.P("End Date: {}".format(point_data[7])))
            years_active = point_data[9]
            try:
                years_active = int(float(years_active))
                if years_active == 0:
                    years_active = '<1'
                contents.append(
                    html.P("Years Active: {}".format(years_active)))
            except ValueError:
                pass
            contents.append(dcc.Graph(
                figure=make_indicator(point_data[4], 'volcano', dark_mode)))

        link = "https://duckduckgo.com/?q={}+{}".format(
            point_data[1], point_data[0])
        contents.append(html.A("More info...", href=link,
                        target="_blank", rel="noopener noreferrer"))

        return html.Div(contents)
