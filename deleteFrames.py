import os
import logging

MAX_IMAGES = 2000
EXT = ".jpeg"

base_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(base_dir, "frame_reduction.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("Starting frame reduction...")
logging.info("Frame reduction started")

for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)

    if not os.path.isdir(folder_path):
        continue

    try:
        images = sorted(
            f for f in os.listdir(folder_path)
            if f.lower().endswith(EXT)
        )

        total = len(images)

        if total <= MAX_IMAGES:
            print(f"{folder}: {total} images (no reduction needed)")
            logging.info(f"{folder}: skipped ({total} images)")
            continue

        # compute evenly spaced indices to keep
        keep_indices = set(
            int(i * (total - 1) / (MAX_IMAGES - 1))
            for i in range(MAX_IMAGES)
        )

        deleted = 0

        for i, img in enumerate(images):
            if i not in keep_indices:
                os.remove(os.path.join(folder_path, img))
                deleted += 1

        print(f"{folder}: {total} → {MAX_IMAGES} images")
        logging.info(f"{folder}: reduced {total} → {MAX_IMAGES}")

    except Exception as e:
        print(f"Error in {folder}: {e}")
        logging.error(f"{folder}: {e}")

logging.info("Frame reduction finished")
print("Done.")