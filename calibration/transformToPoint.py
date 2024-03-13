import cv2
import numpy as np

#takes in input of point and outputs it after transform
#transform is set manually using calibration.py
#Side takes in string "left" or "right"

def get_transformed_point(point, side):
    #MANUAL SET - USE CALIBRATION TO SET VALUES
    if side == "left":
        warp = np.matrix([[-5.26617971e-01,  1.32210137e+00,  2.02825737e+03],
 [-8.25571238e-01, -3.48352529e-01,  3.59499385e+03],
 [ 1.48177440e-05,  1.95378612e-04,  1.00000000e+00]])
    if side == "right":
        warp = np.matrix([[-5.26617971e-01,  1.32210137e+00,  2.02825737e+03],
 [-8.25571238e-01, -3.48352529e-01,  3.59499385e+03],
 [ 1.48177440e-05,  1.95378612e-04,  1.00000000e+00]])

    #dummy points to have a 3x3 and a 3x3 matix. Ignore (0,0) points.
    points = np.float32([[[point[0], point[1]]], [[0,0]], [[0,0]]])
    transformed = cv2.perspectiveTransform(points, warp)
    #board = cv2.imread('board.png')

    pt_x = int(transformed[0][0][0])
    pt_y = int(transformed[0][0][1])
    #print(pt_x, pt_y)
    point = (pt_x, pt_y)

    #Uncomment to show result on img
    img = cv2.imread('calibrated.jpg')
    cv2.circle(img, point, 10, (0, 0, 255), -1)
    
    cv2.namedWindow("img", cv2.WINDOW_NORMAL) 
    cv2.resizeWindow("img", 1088, 816)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    return point

print(get_transformed_point((2056, 1527), "right"))