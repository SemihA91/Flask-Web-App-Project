# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.
from dash.dependencies import Input, Output
import plotly.express as px
from pathlib import Path
import dash
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd



df = pd.read_csv("data/meteor_countries.csv")

df = pd.DataFrame(df["year"].value_counts())
df.index.name = "year"
df.columns = ['count']
df = df.sort_values(by="year")

df.to_csv("meteor_dates.csv")

df = pd.read_csv("data/volcano_data.csv")

df = pd.DataFrame(df["year"].value_counts())
df.index.name = "year"
df.columns = ['count']
df = df.sort_values(by="year")

df.to_csv("volcano_dates.csv")


