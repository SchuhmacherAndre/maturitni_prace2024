from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np

model = YOLO("best.pt")

im1 = Image.open("IMG_0003.jpg")
results = model.predict(source=im1, save=True, conf=0.3)
data = []
classes = []

for result in results:
    data = result.boxes.xyxy.numpy()
    classes = result.boxes.cls.numpy()
    print(result.probs)

def calculate_overlap(box1, box2):
    # Calculate intersection coordinates
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # Calculate intersection area
    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)

    # Calculate box1 area
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])

    # Calculate overlap ratio
    overlap_ratio = intersection_area / box1_area

    return overlap_ratio

def find_dart_tip_pairs(bounding_boxes, classes, min_overlap=0.3):
    pairs = []

    # Get indices of dart tips and darts
    dart_tip_indices = [i for i, cls in enumerate(classes) if cls == 1]
    dart_indices = [i for i, cls in enumerate(classes) if cls == 0]

    # Compare each dart tip with darts
    for dart_tip_index in dart_tip_indices:
        for dart_index in dart_indices:
            overlap_ratio = calculate_overlap(bounding_boxes[dart_tip_index], bounding_boxes[dart_index])
            if overlap_ratio >= min_overlap:
                pairs.append((dart_tip_index, dart_index))

    return pairs

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_closest_dart_tip_corner(dart_tip, dart_box):
    # Get corner points of the dart tip bounding box
    corners = [(dart_tip[0], dart_tip[1]),                # Top-left corner
               (dart_tip[2], dart_tip[1]),                # Top-right corner
               (dart_tip[0], dart_tip[3]),                # Bottom-left corner
               (dart_tip[2], dart_tip[3])]                # Bottom-right corner
    
    # Calculate distances between dart tip corners and dart bounding box corners
    distances = [calculate_distance(corner, (dart_box[0], dart_box[1])) for corner in corners] + \
                [calculate_distance(corner, (dart_box[2], dart_box[1])) for corner in corners] + \
                [calculate_distance(corner, (dart_box[0], dart_box[3])) for corner in corners] + \
                [calculate_distance(corner, (dart_box[2], dart_box[3])) for corner in corners]
    
    # Find the index of the closest corner
    closest_index = np.argmin(distances)
    
    # Get the coordinates of the closest corner
    closest_corner = corners[closest_index % 4]
    
    return closest_corner

def find_closest_points(bounding_boxes, dart_tip_pairs):
    closest_points = []
    
    for tip_index, dart_index in dart_tip_pairs:
        dart_tip = (bounding_boxes[tip_index][0], bounding_boxes[tip_index][1],  # Tip coordinates
                    bounding_boxes[tip_index][2], bounding_boxes[tip_index][3])
        dart_box = (bounding_boxes[dart_index][0], bounding_boxes[dart_index][1],  # Box coordinates
                    bounding_boxes[dart_index][2], bounding_boxes[dart_index][3])
        
        closest_corner = find_closest_dart_tip_corner(dart_tip, dart_box)
        closest_points.append(closest_corner)
    
    return closest_points

dart_tip_pairs = find_dart_tip_pairs(data, classes, min_overlap=0.9)
# Find closest points to corners
closest_points = find_closest_points(data, dart_tip_pairs)
print("Closest Points to Dart Corners:", closest_points)
print("Dart Tip Pairs:", dart_tip_pairs)

