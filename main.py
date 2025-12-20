import numpy
import pandas as pd
import matplotlib.pyplot as plt
import os
import re



current_dir = os.getcwd()


#just a quick verif to check whether the file exist in the current directory and whether the current directory itself exist
if len(current_dir) != 0 and re.search(r"^C:\\",current_dir):
    print("Directory exist\n")
else:
    raise ValueError("Directory empty \n")

print(current_dir)

found = False
for i in os.listdir(current_dir):
    if i == "listings.csv":
        print("CSV file existing\n")
        found = True
        data = pd.read_csv("listings.csv")
        break

if not found:
    print("csv missing\n")
    exit(-1)

print(data.head(15),end="\n")
#print(data.columns,end="\n")
col = data.columns
filt = col.str.contains(r"review",regex=True)
data_filt = data.loc[:,filt].any(axis=1)
print(data.loc[data_filt].head(3),end="\n")

#let us find out about the host
print(data.columns)

print("Here we have 2 kind of data, structed (quantitative/qualitative) and unstructured(text) \n")
print("Hypothesis, we might have to resort to use models applied to numerics/categorical variables thus text mining(TF-IDF so on and so forth) \n")




host_df = data["host_is_superhost"].isna().sum()

data["host_is_superhost"] = data["host_is_superhost"].map({"f":0,"t":1})

distrib = data["host_is_superhost"].value_counts(dropna=False)

print(distrib)
'''
#distribution to explore and understand more
distrib.plot(kind="bar")
plt.title("Distribution of values in host_super_host")
perc = (lambda x: (x / distrib.sum())*100)

for i,v in enumerate(distrib):
    
    plt.text(i,v,f"{perc(v):.1f}%",ha="center")
plt.xlabel("Values")
plt.ylabel("Nb of occurences")
plt.grid(True)
plt.show()

na_mask = data["host_is_superhost"].isna()

na_counts = na_mask.value_counts()
na_counts.index = ["Non-NA", "NA"]
na_counts.plot(kind="bar")
plt.title("NA vs Non-NA for host_is_superhost")
plt.ylabel("Number of rows")
plt.grid(True)
plt.show()
'''

print(data.describe())
print(f"\n{data.dtypes.value_counts()}")

#let us retrieve numerical variables
target = "host_is_superhost"

num_col = data.select_dtypes(include=["number"]).columns.tolist()
num_col = [c for c in num_col if c != target]

quali_col = data.select_dtypes(exclude=["number"]).columns.tolist()

print(data[num_col].describe().T) #Here certain values may be counted as NAN because they are not numerically formated


#based on the results id,scrape_id,host_id are useless variables, therefore they are to be removed as they do not offer any relevant information as they are UNIQUE
#and so what isn't unique is irelevant for predictions as cannot be grouped
data.drop(columns=["id","scrape_id","host_id"],axis=1,inplace=True)

print(data.describe())

#N.B a huge part of NAN variables is to be noticed, which means, it is possible that instead of imputing we could use the text to understand why are those data missing

print(data.columns.sort_values())
