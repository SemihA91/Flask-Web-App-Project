from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash import dcc
from dash import html

# Reads the data from both data sets so 2 graphs can be plotted
dfm = pd.read_csv('data/meteor_dates.csv')
dfv = pd.read_csv('data/volcano_dates.csv')


def make_lines(dfm, dfv, min_year, max_year, dark_mode):
    """
    Make the line graphs for both meteors and volcanoes

    Parameters
    ----------
    dfm : DataFrame
        Meteor data
    dfv : DataFrame
        Volcano data
    min_year : int
        Smaller number on the slider for selecting year range
    max_year : int
        Larger number on the slider for selecting year range
    dark_mode : Boolean
        Selects if dark mode is dislpayed

    Returns
    -------
    figv : .Graph
        The generated figure for the volcano
    figm : .Graph
        The generated figure for the meteor

    """

    # Set range for years
    dfm = dfm[dfm['year'] > min_year]
    dfm = dfm[dfm['year'] < max_year]
    dfv = dfv[dfv['year'] > min_year]
    dfv = dfv[dfv['year'] < max_year]
    # Create figures
    figm = px.line(dfm, x='year', y='count',
                   title='Recorded Meteor Landings By Year')
    figv = px.line(dfv, x='year', y='count',
                   title='Recorded Volcanoes By Year')
    figm.update_layout(hovermode='x unified')
    figv.update_layout(hovermode='x unified')
    figv.update_layout(
        autosize=True,
        height=300,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 50, 'pad': 4},
    )
    figm.update_layout(
        autosize=True,
        height=300,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 50, 'pad': 4},
    )
    # Setting dark mode for both graphs
    if dark_mode:
        figm.update_layout({
            'plot_bgcolor': 'rgb(40,40,40)',
            'paper_bgcolor': 'rgb(40,40,40)',
            'font': {'color': 'white'}
        })
        figv.update_layout({
            'plot_bgcolor': 'rgb(40,40,40)',
            'paper_bgcolor': 'rgb(40,40,40)',
            'font': {'color': 'white'}
        })

    return [dcc.Graph(figure=figv, id='v-line-chart'),
            dcc.Graph(figure=figm, id='m-line-chart')]


def make_line_chart_layout(dark_mode):
    """
    Creates the layout of the line graph page.

    Parameters
    ----------
    dark_mode : Boolean
        Selects if dark mode is dislpayed

    Returns
    -------
    class : html.Div
        The layout of the line graph page.
    """
    return html.Div(children=[
        dcc.Store(id='dark-mode', data=dark_mode), html.Br(),
        html.H3(
            children='Number of Events per Year',
            style={'fontSize': 20}),
        # Insert graphs
        html.Div(
            id='graphs',
            className='card',
            style={'backgroundColor': '#282828' if dark_mode else 'white'}
        ),
        html.Br(),
        # Insert slider
        dcc.RangeSlider(
            id='year-slider',
            min=1950,
            max=dfm['year'].max(),
            marks={
                1950: {'label': '1950', 'style': {'color': '#77b0b1'}},
                1980: {'label': '1980'},
                2000: {'label': '2000'},
                2020: {'label': '2020', 'style': {'color': '#77b0b1'}}
            },
            tooltip={'placement': 'bottom', 'always_visible': True},
            step=1,
            allowCross=False,
            value=[1960, 1980],
        ),
    ])


# Callbacks to update the charts using the year slider position
@app.callback(
    Output('graphs', 'children'),
    Input('year-slider', 'value'),
    State('dark-mode', 'data')
)
def update_graphs(years, dark_mode):
    min_year = years[0]
    max_year = years[1]
    return make_lines(dfm, dfv, min_year, max_year, dark_mode)


if __name__ == '__main__':
    app.run_server(debug=True)
