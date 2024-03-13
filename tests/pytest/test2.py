import cv2

# Mouse callback function
def get_mouse_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pixel coordinates (x, y):", x, y)

# Read the image
image = cv2.imread('IMG_0006.jpg')


cv2.namedWindow("image", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("image", 300, 300)

cv2.imshow("image", image)

cv2.setMouseCallback('image', get_mouse_coordinates)

# Wait for any key to be pressed and close all OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()
