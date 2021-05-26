import cv2

def webcam():

	cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
	ret,frame = cap.read() # return a single frame in variable `frame`

	cv2.imwrite('image.png',frame)
	cv2.destroyAllWindows()

	cap.release()

