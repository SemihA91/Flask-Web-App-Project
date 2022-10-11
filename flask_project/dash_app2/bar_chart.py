from dash.dependencies import Input, Output, State
import plotly.express as px
import dash
import pandas as pd
from dash import dcc
from dash import html


# Reads the data for meteors so they can be plotted.
# Volcanoes not included in this chart becuase they dont
# usually form on land.
df = pd.read_csv('dash_app2/data/meteor_countries.csv')


def filter_years(df, min_year, max_year):
    """
    Update dataframe to include only the filtered years

    Parameters
    ----------
    df : DataFrame
        Meteor data
    min_year : int
        Smaller number on the slider for selecting year range
    max_year : int
        Larger number on the slider for selecting year range

    Returns
    -------
    df : DataFrame
        The updated meteor dataframe

    """
    df = df[df['year'] > min_year]
    df = df[df['year'] < max_year]
    df.reset_index(inplace=True)
    return df


def get_average_masses(df):
    """
    Create new dataframe including the average masses
    of meteors.

    Parameters
    ----------
    df : DataFrame
        Meteor data

    Returns
    -------
    df2 : DataFrame
        The updated meteor dataframe

    """
    n_meteorites = df['countries'].value_counts()
    list_of_countries = n_meteorites.keys()
    masses = []
    number_of_meteorites = []

    for country in list_of_countries:
        total_mass = 0
        number_of_meteorites.append(n_meteorites[country])

        for i in range(len(df['countries'])):
            if df['countries'][i] == country:
                total_mass += df['mass'][i]

        masses.append(total_mass)

    df2 = pd.DataFrame(list_of_countries, columns=['country'])
    df2['mass'] = masses
    df2['number of landings'] = number_of_meteorites
    df2['average mass of meteor'] = df2['mass'] / df2['number of landings']
    df2.sort_values(by=['average mass of meteor'],
                    inplace=True, ascending=False)
    return df2


def filter_masses(df, min_mass, max_mass):
    """
    Update dataframe to include only the filtered masses

    Parameters
    ----------
    df : DataFrame
        meteor data
    min_mass : float
        Smaller number on the slider for selecting mass range
    max_mass : float
        Larger number on the slider for selecting mass range

    Returns
    -------
    df : DataFrame
        The updated dataframe

    """
    df = df[df['mass'] > min_mass]
    df = df[df['mass'] < max_mass]
    df.reset_index(inplace=True)
    return df


def make_bar_chart_layout(dark_mode, dash_app):
    """
    Creates the layout of the bar chart page.

    Parameters
    ----------
    dark_mode : Boolean
        Selects if dark mode is dislpayed

    Returns
    -------
    class : html.Div
        The layout of the bar chart page.
    """
    layout = html.Div(children=[
        dcc.Store(id='dark-mode', data=dark_mode),
        html.H2(
            children='Countries with the Largest Number of Meteorite '
            'Discoveries and Average Masses'),
        # drop down to switch between number of meteors/mass
        dcc.Dropdown(
            id='chart-menu',
            options={
                'number': 'Number of Meteors Discovered per Country',
                'mass': 'Average Mass of Discovered Meteors per Country'
            },
            value='number',
            style={'padding': 2, 'color': 'black'}
        ),
        # Bar graph
        html.Div(
            id='graph',
        ),
        # Sliders
        html.Div([
            html.P('Filter Years', style={
                   'display': 'inline-block', 'float': 'left', 'width': '8%',
                   'padding-left': '20px'}),
            html.Div(
                dcc.RangeSlider(
                    id='year-slider',
                    min=1950,
                    max=df['year'].max(),
                    marks={
                        1950: {'label': '1950', 'style': {'color': '#77b0b1'}},
                        1980: {'label': '1980'},
                        2000: {'label': '2000'},
                        2020: {'label': '2020', 'style': {'color': '#77b0b1'}},

                    },
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    step=1,
                    allowCross=False,
                    value=[1960, 1980]
                ), style={'display': 'inline-block', 'float': 'right',
                          'width': '90%'}
            )
        ]),
        html.Br(),
        html.Br(),
        html.Div([
            html.P('Filter Number of Meteorite Discoveries', style={
                   'display': 'inline-block', 'float': 'left', 'width': '8%',
                   'padding-left': '20px'}, id='number-label'),
            html.Div(
                dcc.RangeSlider(
                    id='landings-slider',
                    min=0,
                    max=0,
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    allowCross=False,
                    value=[4, 266]

                ),
                id='landing-slider-div', style={'display': 'inline-block',
                                                'float': 'right',
                                                'width': '90%'}
            )],
        ),

        html.Div([
            html.P('Filter Average Masses of Discovered Meteorites', style={
                   'display': 'inline-block', 'float': 'left', 'width': '8%',
                   'padding-left': '20px'}, id='mass-label'),
            html.Div(
                dcc.RangeSlider(
                    id='mass-slider',
                    min=0,
                    max=0,
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    allowCross=False,
                ),
                id='mass-slider-div', style={'display': 'inline-block',
                                             'float': 'right', 'width': '90%'}
            ),
        ])
    ])
    init_callbacks(dash_app)
    return layout


def create_occurrences_bar_chart(data, id1, xlabel, ylabel, dark_mode):
    """
    Creates bar chart for number of landings

    Parameters
    ----------
    dark_mode : Boolean
        Selects if dark mode is dislpayed
    id1 : id
        Sets id of the bar chart
    xlabel: String
        Sets the x label of the chart
    ylabel: String
        Sets the y label of the chart
    data : DataFrame
        Selects the data to be used in the chart

    Returns
    -------
    fig : .Graph
        The layout of the line graph page.
    """
    fig = px.bar(data, labels=dict(index=xlabel, value=ylabel),
                 height=500, color=data)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(showlegend=False)
    fig.update(layout_coloraxis_showscale=False)
    if dark_mode:
        fig.update_layout({
            'plot_bgcolor': 'rgba(40, 40, 40, 255)',
            'paper_bgcolor': 'rgba(40, 40, 40, 255)'
        }, font={'color': 'white'}
        )
    return dcc.Graph(
        id=id1,
        figure=fig
    )


def create_mass_bar_chart(data, x_data, y_data, id2, xlabel, ylabel,
                          dark_mode):
    """
    Creates bar chart for the mass of meteors

    Parameters
    ----------
    dark_mode : Boolean
        Selects if dark mode is dislpayed
    id2 : id
        Sets id of the bar chart
    xlabel : String
        Sets the x label of the chart
    ylabel : String
        Sets the y label of the chart
    xdata : DataFrame
        Sets the x data of the chart(countries)
    ydata : DataFrame
        Sets the y data of the chart(mass)
    data : DataFrame
        Selects the data to be used in the chart

    Returns
    -------
    fig : .Graph
        The layout of the line graph page.
    """
    fig = px.bar(data, x=x_data, y=y_data, labels={
                 x_data: xlabel, y_data: ylabel}, height=500, color=x_data)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(showlegend=False)

    if dark_mode:
        fig.update_layout({
            'plot_bgcolor': 'rgba(40, 40, 40, 255)',
            'paper_bgcolor': 'rgba(40, 40, 40, 255)'
        }, font={'color': 'white'}
        )

    return dcc.Graph(
        id=id2,
        figure=fig

    )

# callbacks let the user change the chart from mass to occurance
# and lets the user filter data using 2 sliders


def init_callbacks(app):
    @app.callback(
        [Output('graph', 'children'),
         Output('landings-slider', 'min'),
         Output('landings-slider', 'max'),
         Output('landings-slider', 'marks'),
         Output('landings-slider', 'step'),
         Output('landing-slider-div', 'hidden'),
         Output('number-label', 'hidden'),

         Output('mass-slider', 'min'),
         Output('mass-slider', 'max'),
         Output('mass-slider', 'marks'),
         Output('mass-slider', 'step'),
         Output('mass-slider-div', 'hidden'),
         Output('mass-label', 'hidden')],

        [Input('chart-menu', 'value'),
         Input('year-slider', 'value'),
         Input('landings-slider', 'value'),
         Input('mass-slider', 'value')],
        State('dark-mode', 'data')
    )
    def change_chart(chart, year, landings, masses, dark_mode):
        df2 = df.copy()
        min_year = year[0]
        max_year = year[1]

        if chart == 'mass':
            df2 = filter_years(df2, min_year, max_year)
            df2 = get_average_masses(df2)

            if masses is not None:
                min_mass = masses[0]
                max_mass = masses[1]
            else:
                min_mass = int(df2['average mass of meteor'].min(skipna=True))
                max_mass = int(df2['average mass of meteor'].max(skipna=True))

            masses_data = df2[df2['average mass of meteor'] <= max_mass]
            masses_data = masses_data[
                masses_data['average mass of meteor'] >= min_mass
            ]

            fig = create_mass_bar_chart(masses_data, 'country',
                                        'average mass of meteor', 'mass-graph',
                                        'Country',
                                        'Average Mass of Discovered Meteors',
                                        dark_mode)

            slider_min = int(df2['average mass of meteor'].min())
            slider_max = int(df2['average mass of meteor'].max())
            marks = {
                slider_min: {'label': '{}'.format(slider_min),
                             'style': {'color': '#77b0b1'}},
                slider_max: {'label': '{}'.format(slider_max), 'style': {
                    'color': '#77b0b1'}}
            }
            step = 10000

            return (fig, dash.no_update, dash.no_update, dash.no_update,
                    dash.no_update, True, True, slider_min, slider_max, marks,
                    step, False, False)

        else:
            df2 = filter_years(df2, min_year, max_year)
            if landings is not None:
                min_landings = landings[0]
                max_landings = landings[1]
            else:
                min_landings = int(
                    df2['countries'].value_counts().min(skipna=True))
                max_landings = int(
                    df2['countries'].value_counts().max(skipna=True))

            occurrences = df2['countries'].value_counts()
            occurrences = occurrences[occurrences <= max_landings]
            occurrences = occurrences[occurrences >= min_landings]

            fig = create_occurrences_bar_chart(
                occurrences, 'occurrences-graph', 'Country',
                'Number of Meteorites Discovered', dark_mode)
            slider_min = int(df2['countries'].value_counts().min())
            slider_max = int(df2['countries'].value_counts().max())
            marks = {
                slider_min: {'label': '{}'.format(slider_min),
                             'style': {'color': '#77b0b1'}},
                slider_max: {'label': '{}'.format(slider_max), 'style': {
                    'color': '#77b0b1'}}
            }
            step = 1

            return (fig, slider_min, slider_max, marks, step, False, False,
                    dash.no_update, dash.no_update, dash.no_update,
                    dash.no_update, True, True)


# if __name__ == '__main__':
#     app.run_server(debug=True)
