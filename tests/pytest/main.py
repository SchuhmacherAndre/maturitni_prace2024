import cv2
import time
import numpy as np

cam = cv2.VideoCapture(0)


cam.set(cv2.CAP_PROP_AUTOFOCUS,0)
cam.set( cv2.CAP_PROP_FRAME_WIDTH, 3264  )
cam.set( cv2.CAP_PROP_FRAME_HEIGHT, 2448)


cv2.namedWindow("test")


# Initialize counter
counter = 1

# Function to generate image name
def generate_image_name():
    global counter
    img_name = "IMG_{:04d}.jpg".format(counter)
    counter += 1
    return img_name



while True:
    ret, frame = cam.read()
    f2 = cv2.resize(frame, (1280, 720))

    cam.set(cv2.CAP_PROP_FOCUS, 225)
    cam.set(cv2.CAP_PROP_SETTINGS, 1)
    
    
    cv2.imshow("test", f2)

    if not ret:
        break
    k = cv2.waitKey(1)

    # Check if k%256 == 32 (SPACE pressed)
    if k % 256 == 32:
        # SPACE pressed
        img_name = generate_image_name()
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))