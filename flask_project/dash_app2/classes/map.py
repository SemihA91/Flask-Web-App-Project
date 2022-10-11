import plotly.graph_objects as go
import plotly.express as px


class Map:
    def __init__(self, df_meteor, df_volcano):
        """
    Creates the hover data and sets the map type (2d/3d)

    Parameters
    ----------
    df_meteor : DataFrame
        Meteor data
    df_volcano : DataFrame
        Volcano data

    Returns
    -------

    fig_3d : .Graph
        The 3d map with volcano and meteor points.
    """
        self._df_meteor = df_meteor
        self._df_volcano = df_volcano

        self._mode_3d = False
        self._show_meteor = True
        self._show_volcano = True
        self._dark_theme = False
        self._show_year_colour = False
        self._meteor_hover_data = {
            "Type": False,
            "name": True,
            "reclat": False,
            "reclong": False,
            "massL": False,
            "mass": False,
            "countries": False,
            "year": False,
            "class": False,
            "fall": False

        }
        self._volcano_hover_data = {
            "Type": False,
            "Volcano Name": True,
            "Latitude": False,
            "Longitude": False,
            "VEI": False,
            "VEIsize": False,
            "Start Date": False,
            "End Date": False,
            "Eruption Category": False,
            "Lifetime (years)": False
        }

        self._fig_2d = self._construct_fig_2d()
        self._fig_3d = self._construct_fig_3d()

        # Set default figure to 2D
        self._fig = self._fig_2d

    def _construct_fig_2d(self, center=None):
        """
    Create traces for 2D figures

    Parameters
    ----------
    center : dict
        center map postition
    Returns
    -------
    fig_2d : .Graph
        The 2d map with volcano and meteor points.
    """
        volcano_trace_2d = px.scatter_mapbox(
            self._df_volcano,
            lat="Latitude",
            lon="Longitude",
            zoom=1,
            color=("year" if self._show_year_colour else None),
            color_discrete_sequence=(
                ["red"] if not self._show_year_colour else None),
            size="VEIsize",
            hover_data=self._volcano_hover_data,
            center=center
        ).data[0]

        meteor_trace_2d = px.scatter_mapbox(
            self._df_meteor,
            lat="reclat",
            lon="reclong",
            zoom=1,
            color=("year" if self._show_year_colour else None),
            color_discrete_sequence=(
                ["orange"] if not self._show_year_colour else None),
            size="massL",
            hover_name="countries",
            hover_data=self._meteor_hover_data,
            color_continuous_scale=px.colors.cyclical.IceFire,
            center=center
        ).data[0]

        fig_2d = go.Figure()
        fig_2d.add_traces([meteor_trace_2d, volcano_trace_2d])

        # Configure figures
        fig_2d.update_mapboxes(
            style=("carto-darkmatter" if self._dark_theme
                   else "open-street-map"),
            zoom=2
        )

        fig_2d.update_layout(
            height=550,
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            paper_bgcolor=('#282828' if self._dark_theme else 'white'),
            font={'color': 'white' if self._dark_theme else '#282828'}
        )

        return fig_2d

    def _construct_fig_3d(self):
        """
        Create traces for 3D figures
        -------
        Returns
        -------
        fig_3d : .Graph
            The 3d map with volcano and meteor points.
        """
        meteor_trace_3d = px.scatter_geo(
            self._df_meteor,
            lon='reclong',
            lat='reclat',
            size='massL',
            color=("year" if self._show_year_colour else None),
            color_discrete_sequence=(
                ["orange"] if not self._show_year_colour else None),
            projection="natural earth",
            hover_data=self._meteor_hover_data
        ).data[0]

        volcano_trace_3d = px.scatter_geo(
            self._df_volcano,
            lon='Longitude',
            lat='Latitude',
            size="VEIsize",
            color=("year" if self._show_year_colour else None),
            color_discrete_sequence=(
                ["red"] if not self._show_year_colour else None),
            projection="natural earth",
            hover_data=self._volcano_hover_data
        ).data[0]

        fig_3d = go.Figure()
        fig_3d.add_traces([meteor_trace_3d, volcano_trace_3d])

        fig_3d.update_layout(
            geo=go.layout.Geo(
                projection_type='orthographic',
                showland=True,
                showcountries=True,
                landcolor=('rgb(50, 50, 59)' if self._dark_theme
                           else 'rgb(243, 243, 243)'),
                countrycolor='rgb(204, 204, 204)',
                bgcolor=('#282828' if self._dark_theme
                         else 'white')
            ),
            height=550,
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            paper_bgcolor=('#282828' if self._dark_theme else 'white')
        )

        fig_3d.update_traces(showlegend=False)

        return fig_3d

    def update_dataframes(self, df_meteor, df_volcano):
        """
        Updates the dataframes with filters

        Parameters
        ----------
        df_meteor : DataFrame
            Meteor data
        df_volcano : DataFrame
            Volcano data

        Returns
        -------
        NA
        """
        self._df_meteor = df_meteor
        self._df_volcano = df_volcano
        self._fig_2d = self._construct_fig_2d()
        self._fig_3d = self._construct_fig_3d()
        self._fig.update()

    def set_mode_3d(self, value):
        self._mode_3d = value
        self._fig = self._fig_3d if self._mode_3d else self._fig_2d
        self._fig.update()

    def get_mode_3d(self):
        """
        Sets mode to 3d

        Returns
        -------
        self._mode_3d : Class
        """
        return self._mode_3d

    def get_fig(self):
        """
        Gets map figure from class so it can be used in layout etc

        Returns
        -------
        self._fig : Class
        """
        return self._fig

    def set_show_meteor(self, value):
        """
        Sets if the meteor points are shown

        Parameters
        ----------
        value : Boolean
            Toggles meteor visability

        Returns
        -------
        NA
        """
        self._show_meteor = value
        self._fig_2d.data[0].visible = value
        self._fig_3d.data[0].visible = value

    def set_show_volcano(self, value):
        """
        Sets if the volcano points are shown

        Parameters
        ----------
        value : Boolean
            Toggles volcano visability

        Returns
        -------
        NA
        """
        self._show_volcano = value
        self._fig_2d.data[1].visible = value
        self._fig_3d.data[1].visible = value

    def set_dark_mode(self, value):
        """
        Updates the dark mode setting

        Parameters
        ----------
        value : Boolean
            toggles dark mode

        Returns
        -------
        NA
        """
        self._dark_theme = value

    def set_year_colours(self, value):
        """
        Sets if the heatmap for year of occurance is visible

        Parameters
        ----------
        value : Boolean
            toggles heatmap

        Returns
        -------
        NA
        """
        self._show_year_colour = value
        self._fig_2d = self._construct_fig_2d()
        self._fig_3d = self._construct_fig_3d()
        self._fig.update()

    def set_map_center(self, coordinates):
        """
        Sets the visual of the map to the middle of displayed points.
        Used in the data table pop up

        Parameters
        ----------
        coordinates : float
            Used to provide the middle of the map

        Returns
        -------
        NA
        """
        self._fig_2d.update_layout(
            mapbox=dict(
                center=go.layout.mapbox.Center(
                    lat=coordinates['lat'],
                    lon=coordinates['lon']
                ),
                zoom=3
            )
        )
