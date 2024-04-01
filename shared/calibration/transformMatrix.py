
# importing the module
import cv2
import numpy as np

clicks = 0
points = []
# function to display the coordinates of
# of the points clicked on the image

def reset_values():
    global clicks
    global points
    clicks = 0
    points = []

def click_event(event, x, y, flags, params):
    global clicks
    global points
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        points.append((x,y))
        clicks = clicks + 1
        if(clicks == 4):
            cv2.destroyAllWindows()
            return points


 
def select_points(image):
    # reading the image


    cv2.namedWindow("image", cv2.WINDOW_NORMAL) 
    cv2.resizeWindow("image", 1088, 816)

    cv2.imshow("image", image)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()

img = cv2.imread('img.jpg', 1)

select_points(img)
cam_points = points
reset_values()

board_points = np.array([(1095.36, 2358.72), (1122.24, 763.56), (2701.44, 793.8), (2681.2799999999997, 2366.2799999999997)], dtype=np.float32)
cam_points = np.array([cam_points[0], cam_points[1], cam_points[2],cam_points[3]], dtype=np.float32)

print(cam_points[0], cam_points[1], cam_points[2],cam_points[3])
print("XD")
cam_to_board = cv2.getPerspectiveTransform(cam_points, board_points)
print(cam_to_board)

warp = cv2.warpPerspective(img, cam_to_board, (4024, 3024))
print(cam_to_board)
np.save("transformation_matrix", cam_to_board, allow_pickle=True, fix_imports=True)
cv2.namedWindow("Warp", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Warp", 1088, 816)
cv2.imshow("Warp", warp)
cv2.imwrite("calibrated.jpg", warp)
cv2.waitKey(0)
