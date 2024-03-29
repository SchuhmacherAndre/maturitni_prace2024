from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import pointToScore
import sys

def open_image(file_name):
    try:
        im = Image.open(file_name) 
        return im
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if len(sys.argv) != 2:
    print("Usage: python predict.py <image_file>")
    exit()
else:
    image_file = sys.argv[1]
    im1 = open_image(image_file)


model = YOLO("best.pt") 
results = model.predict(source=im1, save=True, conf=0.4)

data = []
classes = []

for result in results:
    data = result.boxes.xyxy.numpy()
    classes = result.boxes.cls.numpy()

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

# transform to normalized matrix...
def get_transformed_point(point):
   
    board_points = np.array([(1095.36, 2358.72), (1122.24, 763.56), (2701.44, 793.8), (2681.2799999999997, 2366.2799999999997)], dtype=np.float32)
    cam_points = np.array([(1728.0836236933799, 39.75870069605568), (2700.459930313589, 1306.3573085846867), (1352.7804878048782, 2430.9605568445477), (226.87108013937285, 761.0951276102088)], dtype=np.float32)
    cam_to_board = cv2.getPerspectiveTransform(cam_points, board_points)
    warp = cam_to_board
        
    points = np.float32([[[point[0], point[1]]], [[0,0]], [[0,0]]])
    transformed = cv2.perspectiveTransform(points, warp)

    pt_x = int(transformed[0][0][0])
    pt_y = int(transformed[0][0][1])
    point = (pt_x, pt_y)

    return point


dart_tip_pairs = find_dart_tip_pairs(data, classes, min_overlap=0.9)
closest_points = find_closest_points(data, dart_tip_pairs)

normalized_points = []
for point in closest_points:
    normalized_points.append(get_transformed_point(point))

points = []

for point in normalized_points:
    points.append(pointToScore.get_score(point))
    
    
print(points)