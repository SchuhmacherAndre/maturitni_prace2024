import cv2

def set_camera_focus(capture, focus_value):
    try:
        # Check if the camera supports setting focus
        if capture.isOpened():
            capture.set(cv2.CAP_PROP_FOCUS, focus_value)
            return True
        else:
            print("Error: Camera is not opened.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Open the default camera (index 0)
cap = cv2.VideoCapture(0)

# Set the focus value (adjust this according to your camera)
focus_value = 225


set_camera_focus(cap, focus_value)
# Release the camera
cap.release()
