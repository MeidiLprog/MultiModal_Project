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


host_df = data["host_is_superhost"].isna().sum()

data["host_is_superhost"] = data["host_is_superhost"].map({"f":"False","t":"True"})

distrib = data["host_is_superhost"].value_counts(dropna=False)

print(distrib)

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

print(data.describe())
print(f"\n{data.dtypes.value_counts()}")
