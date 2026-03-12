import os
import pickle
import face_recognition

ACTOR_DIR = "data/NS_actors"
CACHE_FILE = "NS_actors_cache.pkl"


def parse_actor_filename(filename):
    base = os.path.splitext(filename)[0]
    if base.endswith("-w"):
        return base[:-2], "w"
    elif base.endswith("-m"):
        return base[:-2], "m"
    return base, "unknown"


def build_actor_cache():
    actor_cache = {}

    for filename in os.listdir(ACTOR_DIR):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        path = os.path.join(ACTOR_DIR, filename)
        print(f"Encoding: {filename}")

        img = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(img)

        if not encs:
            print(f"WARNING: No face found in {filename}")
            continue

        name, gender = parse_actor_filename(filename)

        actor_cache[filename] = {
            "name": name,
            "gender": gender,
            "encoding": encs[0],
        }

    with open(CACHE_FILE, "wb") as f:
        pickle.dump(actor_cache, f)

    print(f"Saved {len(actor_cache)} actors to {CACHE_FILE}")


if __name__ == "__main__":
    build_actor_cache()
