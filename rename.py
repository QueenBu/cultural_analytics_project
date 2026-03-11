import os

# Folder containing your PNG files
folder = "NS_actors"

# Mapping of characters to replace
replacements = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue",
    "ß": "ss"
}

for filename in os.listdir(folder):
    if filename.lower().endswith(".png"):
        new_name = filename
        for old, new in replacements.items():
            new_name = new_name.replace(old, new)

        # Only rename if something actually changed
        if new_name != filename:
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)

            # Avoid overwriting existing files
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_name}")
            else:
                print(f"Skipped (target exists): {new_name}")
