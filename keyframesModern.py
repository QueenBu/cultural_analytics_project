import os
import csv
import face_recognition


def parse_actor_filename(filename):
    base = os.path.splitext(filename)[0]
    if base.endswith("-w"):
        return base[:-2], "F"
    elif base.endswith("-m"):
        return base[:-2], "M"
    return base, "unknown"


def load_actor_encodings(actor_folder):
    actor_data = []

    for filename in os.listdir(actor_folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(actor_folder, filename)
        img = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(img)

        if not encs:
            print(f"WARNING: No face found in actor image {filename}")
            continue

        name, gender = parse_actor_filename(filename)

        actor_data.append({
            "name": name,
            "gender": gender,
            "encoding": encs[0]
        })

    print(f"Loaded {len(actor_data)} actors from {actor_folder}")
    return actor_data


def process_film(film_folder, threshold=0.40):
    print("Starting to process film")
    actor_folder = os.path.join(film_folder, "actors")

    if not os.path.isdir(actor_folder):
        raise ValueError(f"No actors/ folder found in {film_folder}")

    film_name = os.path.basename(film_folder.rstrip("/"))
    output_csv = f"{film_name}.csv"

    actor_data = load_actor_encodings(actor_folder)

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow([
            "frame_name",
            "actor_name",
            "gender",
            "top",
            "right",
            "bottom",
            "left"
        ])
        for frame_file in sorted(os.listdir(film_folder)):
            if not frame_file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            if frame_file == "actors":
                continue

            frame_path = os.path.join(film_folder, frame_file)
            frame = face_recognition.load_image_file(frame_path)

            face_locations = face_recognition.face_locations(frame)
            face_encs = face_recognition.face_encodings(frame, face_locations)

            for i, face_enc in enumerate(face_encs):
                top, right, bottom, left = face_locations[i]

                distances = []
                for actor in actor_data:
                    dist = face_recognition.face_distance([actor["encoding"]], face_enc)[0]
                    distances.append((dist, actor))

                distances.sort(key=lambda x: x[0])
                best_dist, best_actor = distances[0]

                if best_dist < threshold:
                    writer.writerow([
                        frame_file,
                        best_actor["name"],
                        best_actor["gender"],
                        top,
                        right,
                        bottom,
                        left
                    ])

    print(f"Finished {film_name}. Results saved to {output_csv}")

if __name__ == "__main__":
    import argparse
    from multiprocessing import Pool, cpu_count

    parser = argparse.ArgumentParser()
    parser.add_argument("--film-folder", required=True,
                        help="Path to a single film folder OR a parent folder containing many films")
    parser.add_argument("--threshold", type=float, default=0.50)
    parser.add_argument("--workers", type=int, default=0,
                        help="Number of parallel processes (0 = use all cores)")
    args = parser.parse_args()

    # If user gives a single film folder → process only that one
    if os.path.isdir(os.path.join(args.film_folder, "actors")):
        process_film(args.film_folder, threshold=args.threshold)

    else:
        parent = args.film_folder
        movies = []

        for movie in sorted(os.listdir(parent)):
            movie_path = os.path.join(parent, movie)
            actors_path = os.path.join(movie_path, "actors")

            if os.path.isdir(movie_path) and os.path.isdir(actors_path):
                movies.append(movie_path)

        if not movies:
            print("No valid movie folders found.")
            exit()

        # Determine number of workers
        workers = args.workers if args.workers > 0 else cpu_count()
        print(f"Processing {len(movies)} films using {workers} parallel workers.")

        # Wrap process_film so Pool can call it
        def run_movie(path):
            return process_film(path, threshold=args.threshold)

        with Pool(workers) as pool:
            pool.map(run_movie, movies)
