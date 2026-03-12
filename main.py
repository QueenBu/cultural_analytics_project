import os
import csv
import pickle
import face_recognition

CACHE_FILE = "NS_actors_cache.pkl"
KEYFRAME_DIR = "data/NS_Filme/DieUnheimlicheWandlungdesAlexRoscherOscarSima"

MOVIE_NAME = "DieUnheimlicheWandlungdesAlexRoscherOscarSima"
OUTPUT_CSV = f"{MOVIE_NAME}.csv"



def load_actor_cache():
    if not os.path.exists(CACHE_FILE):
        raise FileNotFoundError("actors_cache.pkl not found. Run start.py first.")

    with open(CACHE_FILE, "rb") as f:
        return pickle.load(f)


def process_movie():
    actor_data = load_actor_cache()
    print(f"Loaded {len(actor_data)} actors from cache.")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["frame_name", "actor_name", "gender"])

        for frame_file in sorted(os.listdir(KEYFRAME_DIR)):
            if not frame_file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            frame_path = os.path.join(KEYFRAME_DIR, frame_file)
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
                    if dist < 0.45:  # stricter threshold
                        writer.writerow([frame_file, actor["name"], actor["gender"]])

if __name__ == "__main__":
    process_movie()
