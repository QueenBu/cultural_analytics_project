import pandas as pd
import re

# CSV einlesen
df = pd.read_csv("results_NS_movies_clean.csv", sep=";")

# Zahlen aus position extrahieren
def extract_numbers(s):
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    return list(map(float, nums))

df["position_list"] = df["position"].apply(extract_numbers)

# erstes Element
df["pos0"] = df["position_list"].apply(lambda x: x[0])

# Differenz zu left
df["diff"] = (df["pos0"] - df["left"]).abs()

# pro frame_name + position die Zeile mit minimaler diff behalten
df_clean = df.loc[df.groupby(["frame_name", "position"])["diff"].idxmin()].reset_index(drop=True)

df_clean.to_csv("NS_no_douplicates.csv", sep=";", index=False)


