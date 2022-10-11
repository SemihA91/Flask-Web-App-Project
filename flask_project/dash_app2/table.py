from dash import dash_table, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
from .classes.map import Map

# Reads the data from both data sets so tables can be plotted
dfm = pd.read_csv('data/meteor_countries.csv')
dfv = pd.read_csv('data/volcano_data2.csv')
dfm['Type'] = 'meteorite'
dfv['Type'] = 'volcano'


# [1]
# Choose columns for table and then rename [1]
cols = [
    {'name': i, 'id': i} for i in dfm.loc[:, [
        'name', 'countries', 'reclat', 'reclong', 'mass', 'year', 'fall']]]
cols[0]['name'] = 'Name'
cols[1]['name'] = 'Country'
cols[2]['name'] = 'Latitude'
cols[3]['name'] = 'Longitude'
cols[4]['name'] = 'Mass'
cols[5]['name'] = 'Year'
cols[6]['name'] = 'Fall'

map = Map(dfm, dfv)


def make_table_layout(dark_mode):
    """
    Creates the layout of the data table page.
        Tables showing info about volcanoes is dislpayed
        A map is generated when an entry is selected

    Parameters
    ----------
    dark_mode : Boolean
        Selects if dark mode is dislpayed

    Returns
    -------
    class : html.Div
        The layout of the data table graph page.
    """
    return html.Div([
        dcc.Store(id='dark-mode', data=dark_mode),
        html.H1(
            children='Press the buttons to the left of the table to open'
            ' the map position'),

        html.Br(),
        # Drop down to switch between the 2 tables
        dcc.Dropdown(
            id='table-selector',
            options={
                'meteor': 'Meteor datatable',
                'volcano': 'Volcano datatable'
            },
            value='meteor',
            style={'padding': 2, 'color': 'black'}
        ),

        html.Br(),
        # [2]
        # Meteor table
        html.Div(id='table-m', children=[
            dash_table.DataTable(
                id='table-meteor',
                columns=cols,
                data=dfm.to_dict('records'),
                editable=True,
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                row_selectable='single',
                page_action='native',
                page_current=0,
                page_size=20,

                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                style_filter={
                    'backgroundColor': 'white',
                    'color': 'black'
                },
            )]),
        # Volcano table
        html.Div(id='table-v', children=[dash_table.DataTable(
            id='table-volcano',
            columns=[
                {'name': i, 'id': i} for i in dfv.loc[:, [
                    'Volcano Name', 'VEI', 'Latitude', 'Longitude',
                    'Start Date', 'End Date', 'Lifetime (years)',
                    'Evidence Method (dating)', 'Eruption Category']]],
            data=dfv.to_dict('records'),
            editable=True,
            filter_action='native',
            sort_action='native',
            row_selectable='single',
            sort_mode='multi',
            page_action='native',
            page_current=0,
            page_size=20,
            style_data={
                        'color': 'black',
                        'backgroundColor': 'white',
            },
            style_data_conditional=[{
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            },
            style_filter={
                'backgroundColor': 'white',
                'color': 'black'
            },
        )]),
        # Pop up map
        dbc.Modal(
            children=[
                dbc.ModalHeader(dbc.ModalTitle('Location on map')),
                dbc.ModalBody(
                    id='modal-body'
                )
            ],
            id='Modal',
            centered=True,
            size='lg',
            is_open=False,
        ),
    ])

# Callbacks allow the user to switch between tables and
# display a map of selected data


@app.callback(
    [Output('table-m', 'hidden'),
     Output('table-v', 'hidden'),
     Output('Modal', 'children'),
     Output('Modal', 'is_open'),
     Output('table-meteor', 'style_data'),
     Output('table-meteor', 'style_data_conditional'),
     Output('table-meteor', 'style_filter'),
     Output('table-volcano', 'style_data'),
     Output('table-volcano', 'style_data_conditional'),
     Output('table-volcano', 'style_filter')],

    [Input('table-selector', 'value'),
     Input('table-meteor', 'selected_rows'),
     Input('table-volcano', 'selected_rows')],

    [State('Modal', 'is_open'),
     State('dark-mode', 'data')]
)
def update_layout(table, n1, n2, is_open, dark_mode):

    if dark_mode:
        style_data = {
            'color': 'white',
            'backgroundColor': '#282828',
        }
        style_data_conditional = [{
            'if': {'row_index': 'even'},
            'backgroundColor': '#353535'
        }]
        style_filter = {
            'backgroundColor': '#282828',
            'color': 'white'
        }
    else:
        style_data = {
            'color': 'black',
            'backgroundColor': 'white',
        }
        style_data_conditional = [{
            'if': {'row_index': 'even'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }]
        style_filter = {
            'backgroundColor': 'white',
            'color': 'black'
        }

    if table == 'meteor':
        if n1:
            filtered_df = dfm.iloc[n1]
            map.update_dataframes(filtered_df, dfv)
            map.set_year_colours(False)
            map.set_mode_3d(False)
            map.set_show_meteor(True)
            map.set_show_volcano(False)
            map.set_map_center(
                {'lat': filtered_df['reclat'].values[0],
                 'lon': filtered_df['reclong'].values[0]})

            return (False, True, [dbc.ModalHeader(
                dbc.ModalTitle('Location on map')),
                dbc.ModalBody(dcc.Graph(
                    figure=map.get_fig()))], not is_open, style_data,
                style_data_conditional, style_filter, style_data,
                style_data_conditional, style_filter)
        else:
            return (False, True, [dbc.ModalHeader(
                dbc.ModalTitle('Location on map')),
                dbc.ModalBody(dcc.Graph(
                    figure=map.get_fig()))], is_open, style_data,
                style_data_conditional, style_filter, style_data,
                style_data_conditional, style_filter)

    elif table == 'volcano':
        if n2:
            filtered_df = dfv.iloc[n2]
            map.update_dataframes(dfm, filtered_df)
            map.set_year_colours(False)
            map.set_mode_3d(False)
            map.set_show_meteor(False)
            map.set_show_volcano(True)
            map.set_map_center(
                {'lat': filtered_df['Latitude'].values[0],
                 'lon': filtered_df['Longitude'].values[0]})
            return (True, False, [dbc.ModalHeader(
                dbc.ModalTitle('Location on map')),
                dbc.ModalBody(dcc.Graph(
                    figure=map.get_fig()))], not is_open, style_data,
                style_data_conditional, style_filter, style_data,
                style_data_conditional, style_filter)
        else:
            return (True, False, [dbc.ModalHeader(
                dbc.ModalTitle('Location on map')),
                dbc.ModalBody(dcc.Graph(
                    figure=map.get_fig()))], is_open, style_data,
                style_data_conditional, style_filter, style_data,
                style_data_conditional, style_filter)


# https://dash.plotly.com/datatable/interactivity

# https://community.plotly.com/t/rename-dash-table-columns/39604/6
