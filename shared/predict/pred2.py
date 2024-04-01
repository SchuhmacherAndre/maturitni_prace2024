from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import pointToScore
import sys
import math


# transform to normalized matrix...
def get_transformed_point(point):
   
    board_points = np.array([(1095.36, 2358.72), (1122.24, 763.56), (2701.44, 793.8), (2681.2799999999997, 2366.2799999999997)], dtype=np.float32)
    cam_points = np.array([(1482, 72), (2550, 1194), (1362, 2427), (69, 918)], dtype=np.float32)
    cam_to_board = cv2.getPerspectiveTransform(cam_points, board_points)
    warp = cam_to_board
        
    points = np.float32([[[point[0], point[1]]], [[0,0]], [[0,0]]])
    transformed = cv2.perspectiveTransform(points, warp)

    pt_x = int(transformed[0][0][0])
    pt_y = int(transformed[0][0][1])
    point = (pt_x, pt_y)

    return point

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

im1 = Image.open("img.jpg") 


model = YOLO("best.pt") 
results = model.predict(source=im1, save=True, conf=0.1)
import math
def calculate_distance(box1, box2):
    # Extract coordinates of box1 and box2
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Calculate centroids
    center1_x = x1 + w1 / 2
    center1_y = y1 + h1 / 2
    center2_x = x2 + w2 / 2
    center2_y = y2 + h2 / 2

    # Calculate Euclidean distance between centroids
    distance = math.sqrt((center1_x - center2_x)**2 + (center1_y - center2_y)**2)
    
    return distance

def find_nearest_dart_tip(dart_box, dart_tips_boxes, threshold):
    nearest_tip = None
    min_distance = threshold
    for tip_box in dart_tips_boxes:
        distance = calculate_distance(dart_box, tip_box)
        if distance < min_distance:
            nearest_tip = tip_box
            min_distance = distance
    return nearest_tip


data = []
classes = []
filtered_classes = []
filtered_boxes = []
    
for result in results:
    confidences = result.boxes.conf.numpy()
    data = result.boxes.xyxy.numpy()
    classes = result.boxes.cls.numpy()
    
    class_thresholds = {0: 0.7, 1: 0.3}

    
    for conf, cls_id, boxes in zip(confidences, classes, data):
        # Check if the confidence is above the threshold for the respective class
        if cls_id == 0 and conf >= class_thresholds.get(0, 0.7):
            filtered_classes.append(cls_id)
            filtered_boxes.append(boxes)
        elif cls_id == 1 and conf >= class_thresholds.get(1, 0.3):
            filtered_classes.append(cls_id)
            filtered_boxes.append(boxes)
    
filtered_boxes = [box.tolist() for box in filtered_boxes]

def get_center(bbox):
    # bbox is a tuple or list containing (x1, y1, x2, y2)
    x1, y1, x2, y2 = bbox
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y

def get_stuck(bbox):
    corners = [
         [bbox[0], bbox[1]],
         [bbox[2], bbox[1]],
         [bbox[2], bbox[3]],
         [bbox[0], bbox[3]]
    ]
    
    target_point = (0, 2448)

    # Calculate distances and find the closest point
    closest_point = None
    closest_distance = float('inf')

    for coord in corners:
        distance = math.dist(coord, target_point)
        if distance < closest_distance:
            closest_distance = distance
            closest_point = coord
    
    return closest_point
    

tip_boxes = []

for box, class_num in zip(filtered_boxes, filtered_classes):
    if class_num == 1.0:
        tip_boxes.append(box)

normalized_points = []

for box in tip_boxes:
    normalized_points.append(get_transformed_point(get_stuck(box)))

points = []

for point in normalized_points:
    points.append(pointToScore.get_score(point))
    
pointsByRing = []
pointsByCount = []

for i in points:
    if i[0][0] == "s":
        pointsByRing.append(i[0][0].upper() + str(i[1]))
    elif i[0][0] == "d":
        pointsByRing.append(i[0][0].upper() + str(int(i[1]/2)))
    elif i[0][0] == "t":
        pointsByRing.append(i[0][0].upper() + str(int(i[1]/3)))
    
    
    pointsByCount.append(i[1])

print(pointsByRing)
print(pointsByCount)