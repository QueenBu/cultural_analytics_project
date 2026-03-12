import os
import csv
import pickle
import argparse
import face_recognition
from multiprocessing import Pool, cpu_count


CACHE_FILE = "NS_actors_cache.pkl"
TOLERANCE = 0.6


def load_actor_cache():
    if not os.path.exists(CACHE_FILE):
        raise FileNotFoundError("NS_actors_cache.pkl not found. Run start.py first.")

    with open(CACHE_FILE, "rb") as f:
        return pickle.load(f)


def process_single_movie(args):
    movie_folder, actor_data = args
    movie_name = os.path.basename(movie_folder.rstrip("/"))
    output_csv = f"{movie_name}.csv"

    print(f"Processing movie: {movie_name}")

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["frame_name", "actor_name", "gender"])

        for frame_file in sorted(os.listdir(movie_folder)):
            if not frame_file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            frame_path = os.path.join(movie_folder, frame_file)
            frame = face_recognition.load_image_file(frame_path)

            face_locations = face_recognition.face_locations(frame)
            face_encs = face_recognition.face_encodings(frame, face_locations)

            for face_enc in face_encs:
                distances = []

                # compute distance to every actor
                for actor in actor_data.values():
                    dist = face_recognition.face_distance([actor["encoding"]], face_enc)[0]
                    distances.append((dist, actor))

                # sort by distance (closest first)
                distances.sort(key=lambda x: x[0])

                # keep only the best 5 matches
                top5 = distances[:5]

                # write only those below the stricter threshold
                for dist, actor in top5:
                    if dist < 0.40:  # stricter threshold
                        writer.writerow([frame_file, actor["name"], actor["gender"]])

    print(f"Finished: {movie_name}")
    return movie_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--movies-folder", required=True, help="Top folder containing movie subfolders")
    args = parser.parse_args()

    movies_folder = args.movies_folder
    actor_data = load_actor_cache()

    # Find all movie subfolders
    movie_dirs = [
        os.path.join(movies_folder, d)
        for d in os.listdir(movies_folder)
        if os.path.isdir(os.path.join(movies_folder, d))
    ]

    print(f"Found {len(movie_dirs)} movies.")

    # Multiprocessing
    pool_args = [(movie_dir, actor_data) for movie_dir in movie_dirs]

    with Pool(cpu_count()) as pool:
        pool.map(process_single_movie, pool_args)


if __name__ == "__main__":
    main()
