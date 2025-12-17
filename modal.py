import random 
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("listings.csv")

print(df.head(15))
print(df.shape)
filt = df.isna().sum() != 0
print(df.loc[:,filt])
df.columns = [x.lower() for x in df.columns]
print(df.columns)