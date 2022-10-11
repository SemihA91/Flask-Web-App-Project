#Mass labels are added based on the range they fall in
import pandas as pd
import numpy as np

df = pd.read_csv("data/newMet.csv")

df["massL"] = df["mass"]
 
df["massL"] = np.where(df['massL'].between(0,100), 1, df['massL'])
df["massL"] = np.where(df['massL'].between(100,1000), 1, df['massL'])
df["massL"] = np.where(df['massL'].between(1000,10000), 1, df['massL'])
df["massL"] = np.where(df['massL'].between(10000,100000), 3, df['massL'])
df["massL"] = np.where(df['massL'].between(100000,1000000), 7, df['massL'])
df["massL"] = np.where(df['massL'].between(1000000,10000000), 10, df['massL'])
df["massL"] = np.where(df['massL'].between(10000000,100000000), 15, df['massL'])

print(df["massL"].unique())

df["massL"].values
print(df)

df.to_csv("newMet2.csv")
