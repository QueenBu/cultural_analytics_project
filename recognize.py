import cv2
import os
import numpy as np
import pickle
import csv

movie_name = "DergroeSchattenHeinrichGeorge"
path = r"C:\Users\bianc\Videos\videos\NS Filme\DergroeSchattenHeinrichGeorge"
keyframes_dir = path

# ---------- load actors database ----------
with open("actor_db.pkl", "rb") as f:
    database = pickle.load(f)

# database structure: {actor_name: {"gender": g, "embedding": vec}}

actor_names = []
actor_genders = []
actor_embeddings = []

for actor, data in database.items():
    actor_names.append(actor)
    actor_genders.append(data["gender"])
    actor_embeddings.append(data["embedding"])

actor_embeddings = np.array(actor_embeddings)

# ---------- load models ----------
detector = cv2.dnn.readNetFromCaffe(
    r"C:\Users\bianc\Videos\videos\models\deploy.prototxt",
    r"C:\Users\bianc\Videos\videos\models\res10_300x300_ssd_iter_140000.caffemodel"
)

embedder = cv2.dnn.readNetFromTorch(
    r"C:\Users\bianc\Videos\videos\models\nn4.small2.v1.t7"
)

# ---------- process frames ----------
csv_file = movie_name + ".csv"
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    for frame_file in sorted(os.listdir(keyframes_dir)):

        path = os.path.join(keyframes_dir, frame_file)
        image = cv2.imread(path)

        if image is None:
            continue

        found_actors = set()

        (h, w) = image.shape[:2]

        # smaller image = faster detection
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300,300)),
            1.0,
            (300,300),
            (104,177,123)
        )

        detector.setInput(blob)
        detections = detector.forward()

        for i in range(detections.shape[2]):

            confidence = detections[0,0,i,2]

            if confidence < 0.5:
                continue

            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (x1,y1,x2,y2) = box.astype(int)

            face = image[y1:y2, x1:x2]

            if face.shape[0] < 40 or face.shape[1] < 40:
                continue

            face_blob = cv2.dnn.blobFromImage(
                face,
                1.0/255,
                (96,96),
                (0,0,0),
                swapRB=True
            )

            embedder.setInput(face_blob)
            vec = embedder.forward().flatten()

            dists = np.linalg.norm(actor_embeddings - vec, axis=1)
            best_idx = np.argmin(dists)
            best_dist = dists[best_idx]

            if best_dist < 0.6:

                actor = actor_names[best_idx]
                gender = actor_genders[best_idx]

                if actor not in found_actors:
                    writer.writerow([frame_file, actor, gender])
                    found_actors.add(actor)

print("Results written to" + csv_file)