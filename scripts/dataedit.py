import pandas as pd
import numpy as np

df = pd.read_csv("data/meteorite_data.csv")

df['mass'].replace('', np.nan, inplace=True)
df.dropna(subset=['mass'], inplace=True)

df.to_csv('newMet.csv')

