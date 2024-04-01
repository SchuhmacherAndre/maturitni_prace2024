# importing the module
import cv2
import pointToScore
# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell

        point = (x,y)
        print(point)
        score = pointToScore.get_score(point)
        print(score)
        #point_to_score.score_to_text(score)
 
        # displaying the coordinates
        # on the image window
        cv2.imshow('image', img)
 
    # checking for right mouse clicks    
 
# driver function
if __name__=="__main__":
 
    # reading the image
    img = cv2.imread('iPhoneDartboard.jpg', 1)
    # displaying the image

    cv2.namedWindow("image", cv2.WINDOW_NORMAL) 
    cv2.resizeWindow("image", 1920, 1080)
    cv2.imshow('image', img)
 
  
    cv2.setMouseCallback('image', click_event)
 
    cv2.waitKey(0)
 
 
    cv2.destroyAllWindows()