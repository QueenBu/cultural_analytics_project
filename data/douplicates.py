import pandas as pd
import re

# CSV einlesen
df = pd.read_csv("results_modern_movies_clean.csv", sep=";")

# --- helper: extract numbers from position string ---
def extract_numbers(s):
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    return list(map(float, nums))

df["position_list"] = df["position"].apply(extract_numbers)
df["pos0"] = df["position_list"].apply(lambda x: x[0])

# --- helper: reduce a consecutive run by choosing row with smallest |pos0 - left| ---
def pick_best(rows):
    diffs = (rows["pos0"] - rows["left"]).abs()
    return rows.loc[diffs.idxmin()]

# --- PASS A: collapse runs with same frame_name + same position ---
keep_rows = []
i = 0
n = len(df)

while i < n:
    j = i + 1
    # find end of run
    while j < n and df.loc[j, "frame_name"] == df.loc[i, "frame_name"] and df.loc[j, "position"] == df.loc[i, "position"]:
        j += 1
    run = df.iloc[i:j]
    best = pick_best(run)
    keep_rows.append(best)
    i = j

dfA = pd.DataFrame(keep_rows).reset_index(drop=True)

# --- PASS B: collapse runs with same frame_name + same bounding box ---
keep_rows = []
i = 0
n = len(dfA)

while i < n:
    j = i + 1
    while (
        j < n
        and dfA.loc[j, "frame_name"] == dfA.loc[i, "frame_name"]
        and dfA.loc[j, "top"] == dfA.loc[i, "top"]
        and dfA.loc[j, "right"] == dfA.loc[i, "right"]
        and dfA.loc[j, "bottom"] == dfA.loc[i, "bottom"]
        and dfA.loc[j, "left"] == dfA.loc[i, "left"]
    ):
        j += 1
    run = dfA.iloc[i:j]
    best = pick_best(run)
    keep_rows.append(best)
    i = j

df_final = pd.DataFrame(keep_rows).reset_index(drop=True)

df_final.to_csv("modern_no_douplicates.csv", sep=";", index=False)


