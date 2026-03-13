import pandas as pd
import glob
import os

# Folder containing your CSV files
folder_path = r"C:\Users\bianc\Videos\videos\data\Results_NS_face_recognition"

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

df_list = []

for file in csv_files:
    df = pd.read_csv(file, sep=None, engine="python")  # auto-detect delimiter
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

combined_df.to_csv("combined.csv", index=False)
