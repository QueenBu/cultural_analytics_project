import cv2
import os
import numpy as np
import pickle

keyframes_dir = r"C:\Users\bianc\Videos\videos\moderneFilme\Her"

with open("actor_db.pkl", "rb") as f:
    database = pickle.load(f)

detector = cv2.dnn.readNetFromCaffe(
    r"C:\Users\bianc\Videos\videos\models\deploy.prototxt",
    r"C:\Users\bianc\Videos\videos\models\res10_300x300_ssd_iter_140000.caffemodel"
)

embedder = cv2.dnn.readNetFromTorch(
    r"C:\Users\bianc\Videos\videos\models\nn4.small2.v1.t7"
)

for frame_file in os.listdir(keyframes_dir):

    path = os.path.join(keyframes_dir, frame_file)
    image = cv2.imread(path)

    if image is None:
        continue

    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(
        cv2.resize(image,(300,300)),
        1.0,
        (300,300),
        (104,177,123)
    )

    detector.setInput(blob)
    detections = detector.forward()

    actors_in_frame = []

    for i in range(detections.shape[2]):

        confidence = detections[0,0,i,2]

        if confidence < 0.5:
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

        best_actor = None
        best_dist = 999

        for actor, emb in database.items():

            dist = np.linalg.norm(vec - emb)

            if dist < best_dist:
                best_dist = dist
                best_actor = actor

        if best_dist < 0.6:
            actors_in_frame.append(best_actor)

    print(frame_file, actors_in_frame)