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

df = pd.read_csv("data/volcano_data.csv")

# print(df["VEI"].value_counts())

df["VEIsize"] = df["VEI"]
# df["VEIsize"] +=1

df=df.replace(to_replace="VEI Unknown",value=2.0)

print(df.shape)
print(df["VEIsize"].value_counts())



df['VEIsize'] = df["VEIsize"].apply(lambda x: 1+ float(x)**2)

# df['VEIsize'].replace(8.0, 8, inplace=True)
# df['VEIsize'].replace(7.0, 7, inplace=True)
# df['VEIsize'].replace(6.0, 6, inplace=True)
# df['VEIsize'].replace(5.0, 5, inplace=True)
# df['VEIsize'].replace(4.0, 4, inplace=True)
# df['VEIsize'].replace(3.0, 3, inplace=True)
# df['VEIsize'].replace(2.0, 2, inplace=True)
# df['VEIsize'].replace(0.0, 1.0, inplace=True)



print(df["VEIsize"].value_counts())

# print(df["VEIsize"].dtypes)

df.to_csv("volcano_data2.csv")