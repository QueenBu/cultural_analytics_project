import os

# Folder containing the images
base_dir = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(base_dir, "!Interstellar")

# Image extensions to consider
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")

# Get sorted list of images
images = sorted([f for f in os.listdir(folder) if f.lower().endswith(image_extensions)])

# Delete every second image
for i, image in enumerate(images):
    if i % 2 == 1:  # every second file
        path = os.path.join(folder, image)
        os.remove(path)
        print(f"Deleted: {image}")

print("Finished.")