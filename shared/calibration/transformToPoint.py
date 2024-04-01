import cv2
import numpy as np

def get_transformed_point(point):
    warp = np.matrix([[-9.08300076e-01,  1.05953663e+00,  2.55610570e+03],
    [-6.69093278e-01, -5.39046833e-01,  3.39528167e+03],
    [-6.06695297e-05,  1.91137796e-04,  1.00000000e+00]])
        
    points = np.float32([[[point[0], point[1]]], [[0,0]], [[0,0]]])
    transformed = cv2.perspectiveTransform(points, warp)

    pt_x = int(transformed[0][0][0])
    pt_y = int(transformed[0][0][1])
    point = (pt_x, pt_y)

    return point

print(get_transformed_point((1380, 1399), "right"))