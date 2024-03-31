from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import time

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
cam.set(cv2.CAP_PROP_FOCUS, 225)

count = 0

while True:
    count += 1
    ret, frame = cam.read()
    f2 = cv2.resize(frame, (1280, 720))
    cam.set(cv2.CAP_PROP_FOCUS, 225)

    if count == 25:
        cv2.imwrite("img.jpg", frame)
        break

model = YOLO("best.pt") 
results = model.predict(source="img.jpg", save=True, conf=0.4)
for result in results:
    confidences = result.boxes.conf.numpy()
    class_ids = result.boxes.cls.numpy()
    
    class_thresholds = {0: 0.7, 1: 0.3}
    filtered_boxes = []
    cls = []
    for conf, cls_id in zip(confidences, class_ids):
        # Check if the confidence is above the threshold for the respective class
        if cls_id == 0 and conf >= class_thresholds.get(0, 0.7):
            filtered_boxes.append((conf, cls_id))
        elif cls_id == 1 and conf >= class_thresholds.get(1, 0.3):
            filtered_boxes.append((conf, cls_id))
    
    for conf, cls_id in filtered_boxes:
        cls.append(int(cls_id))
    
    count = 0
    for num in cls:
        if num == 0:
            count += 1
            
    print(count)