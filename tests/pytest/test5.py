import cv2
import numpy as np

#takes in input of point and outputs it after transform
#transform is set manually using calibration.py
#Side takes in string "left" or "right"

def get_transformed_point(point, side):
    #MANUAL SET - USE CALIBRATION TO SET VALUES
    if side == "left":
        warp = np.matrix([[-6.15728140e-01,  1.36252703e+00,  5.25274862e+02],
                    [-7.27337731e-01, -3.55884490e-01,  1.03128486e+03],
                    [ 8.11844821e-05,  5.04222387e-04,  1.00000000e+00]])
    if side == "right":
        warp = np.matrix([[-6.15728140e-01,  1.36252703e+00,  5.25274862e+02],
        [-7.27337731e-01, -3.55884490e-01,  1.03128486e+03],
        [ 8.11844821e-05,  5.04222387e-04,  1.00000000e+00]])


    #dummy points to have a 3x3 and a 3x3 matix. Ignore (0,0) points.
    points = np.float32([[[point[0], point[1]]], [[0,0]], [[0,0]]])
    transformed = cv2.perspectiveTransform(points, warp)
    #board = cv2.imread('board.png')

    pt_x = int(transformed[0][0][0])
    pt_y = int(transformed[0][0][1])
    #print(pt_x, pt_y)
    point = (pt_x, pt_y)
    
    img = cv2.imread('dart.jpg')
    cv2.circle(img, point, 1, (0, 0, 255), -1)
    cv2.imshow("img", img)
    cv2.waitKey(0)

    return point

print(get_transformed_point((563, 237), "right"))