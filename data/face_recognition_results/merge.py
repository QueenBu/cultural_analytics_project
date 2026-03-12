import pandas as pd
import glob
import os

# Folder containing your CSV files
folder_path = r"C:\Users\bianc\Videos\videos\data\face_recognition_results"

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Read and concatenate
df_list = [pd.read_csv(file) for file in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

# Save to a new CSV
combined_df.to_csv("combined.csv", index=False)
