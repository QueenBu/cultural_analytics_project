import os
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 4 


base_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(base_dir, "../ffmpeg_keyframe_extract.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("Starting parallel processing...")
logging.info("Script started")


def process_folder(folder):
    folder_path = os.path.join(base_dir, folder)

    if not os.path.isdir(folder_path):
        return f"Skipping {folder} (not a folder)"

    try:
        files = os.listdir(folder_path)

        # skip folders already containing jpeg
        if any(f.lower().endswith(".jpeg") for f in files):
            logging.info(f"Skipped {folder} - JPEGs already exist")
            return f"Skipped {folder} (JPEGs exist)"

        mp4_files = sorted([f for f in files if f.lower().endswith(".mp4")])

        if not mp4_files:
            logging.info(f"No MP4 found in {folder}")
            return f"No MP4 in {folder}"

        first_mp4 = mp4_files[0]
        input_path = os.path.join(folder_path, first_mp4)

        filename_no_ext = os.path.splitext(first_mp4)[0]
        output_pattern = os.path.join(folder_path, f"{filename_no_ext}-%02d.jpeg")

        cmd = [
            "ffmpeg",
            "-skip_frame", "nokey",
            "-i", input_path,
            "-fps_mode", "vfr",
            "-frame_pts", "true",
            output_pattern
        ]

        logging.info(f"Processing {folder}: {first_mp4}")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        logging.info(f"Finished {folder}")
        return f"Finished {folder}"

    except Exception as e:
        logging.error(f"Error processing {folder}: {e}")
        return f"Error in {folder}: {e}"


# collect folders
folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(process_folder, folder): folder for folder in folders}

    for future in as_completed(futures):
        print(future.result())

logging.info("Script finished")
print("All tasks complete.")