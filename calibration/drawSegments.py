import cv2
import numpy as np

# Function to overlay grid on dartboard image
def overlay_grid(image, grid_params):
    # Draw concentric circles for point values
    for radius in grid_params['circles']:
        cv2.circle(image, grid_params['center'], radius, (0, 255, 0), 2)
    # Draw radial lines to divide segments
    for angle in grid_params['angles']:
        x = int(grid_params['center'][0] + grid_params['radius'] * np.cos(angle))
        y = int(grid_params['center'][1] + grid_params['radius'] * np.sin(angle))
        cv2.line(image, grid_params['center'], (x, y), (0, 255, 0), 2)


# Example parameters
grid_params = {
    'center': (2045 , 1520),  # Center of the dartboard
    'radius': 1080 ,          # Radius of the dartboard
    'circles': [40, 640, 1020],  # Radii of concentric circles
    'angles': np.linspace(0, 2*np.pi, 21)  # Angles for radial lines
}

def get_mouse_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pixel coordinates (x, y):", x, y)
# Load dartboard image
dartboard_image = cv2.imread('calibrated.jpg')

# Call function to overlay grid
overlay_grid(dartboard_image, grid_params)

# Display image with grid
cv2.namedWindow("image", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("image", 1088, 816)
cv2.imshow('image', dartboard_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
