import os
import shutil
import re

# Folder containing the files
base_dir = os.path.dirname(os.path.abspath(__file__))
target_folder = os.path.join(base_dir, "moderneFilme")

for item in os.listdir(target_folder):
    item_path = os.path.join(target_folder, item)

    # Only process files
    if os.path.isfile(item_path):
        name, ext = os.path.splitext(item)

        # Keep only letters
        clean_name = re.sub(r'[^a-zA-Z]', '', name)

        # Skip if nothing remains
        if not clean_name:
            continue

        # New filename
        new_filename = clean_name + ext
        new_file_path = os.path.join(target_folder, new_filename)

        # Rename file if needed
        if item != new_filename:
            os.rename(item_path, new_file_path)
        else:
            new_file_path = item_path

        # Create folder
        folder_path = os.path.join(target_folder, clean_name)
        os.makedirs(folder_path, exist_ok=True)

        # Move file into folder
        shutil.move(new_file_path, os.path.join(folder_path, new_filename))

print("Done!")