import pycountry_convert as pc
from pathlib import Path
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np


# Data from https://worldpopulationreview.com/country-rankings/list-of-countries-by-continent

df = pd.read_csv("data/meteor_countries.csv")
dfcont = pd.read_csv("data/Continents.csv")


# df["continent"] = df["countries"]

# if df["continent"].equals(dfcont["country"]):
#     df["continent"] = dfcont["continent"]

print(df)



