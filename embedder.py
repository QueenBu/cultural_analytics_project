import cv2
import os
import numpy as np
import pickle

actors_dir = r"C:\Users\bianc\Videos\videos\NS_actors"

detector = cv2.dnn.readNetFromCaffe(
    r"C:\Users\bianc\Videos\videos\models\deploy.prototxt",
    r"C:\Users\bianc\Videos\videos\models\res10_300x300_ssd_iter_140000.caffemodel"
)

embedder = cv2.dnn.readNetFromTorch(
    r"C:\Users\bianc\Videos\videos\models\nn4.small2.v1.t7"
)

database = {}

for file in os.listdir(actors_dir):

    path = os.path.join(actors_dir, file)
    image = cv2.imread(path)

    if image is None:
        print("Skipping:", file)
        continue

    #firstname_lastname-w.png
    #firstname_lastname-m.png
    name_part = file.split(".")[0]
    actor_name, gender = name_part.split("-")

    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300,300)),
        1.0,
        (300,300),
        (104,177,123)
    )

    detector.setInput(blob)
    detections = detector.forward()

    if detections.shape[2] == 0:
        print("No face detected:", file)
        continue

    i = np.argmax(detections[0,0,:,2])
    confidence = detections[0,0,i,2]

    if confidence < 0.5:
        print("Low confidence:", file)
        continue

    box = detections[0,0,i,3:7] * np.array([w,h,w,h])
    (x1,y1,x2,y2) = box.astype(int)

    face = image[y1:y2, x1:x2]

    face_blob = cv2.dnn.blobFromImage(
        face,
        1.0/255,
        (96,96),
        (0,0,0),
        swapRB=True
    )

    embedder.setInput(face_blob)
    vec = embedder.forward().flatten()

    database[actor_name] = {
        "gender": gender,
        "embedding": vec
    }

print("Actors loaded:", len(database))

with open("actor_db.pkl", "wb") as f:
    pickle.dump(database, f)

print("Database saved.")