from tensorflow.keras.models import load_model
import cv2
import numpy as np

try:
    model = load_model("models/self_driving_model.h5")
except:
    model = None

def predict_steering(frame):
    if model is None:
        return 0.0

    img = cv2.resize(frame, (200, 66))
    img = img / 255.0
    img = img.reshape(1, 66, 200, 3)

    steering = float(model.predict(img, verbose=0))
    return steering