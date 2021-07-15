import numpy as np #pip install numpy
import cv2          #pip install opencv-python
import imutils       #pip install imutils
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

#web cam
def webcam_live(hog):
    # open webcam video stream
    cap = cv2.VideoCapture(0)

    # the output will be written to output.avi
    out = cv2.VideoWriter(
        'output.avi',
        cv2.VideoWriter_fourcc(*'MJPG'),
        15.,
        (640,480))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)
        
        # Write the output video 
        out.write(frame.astype('uint8'))
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    # and release the output
    out.release()
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)

#image
def img_live(hog):
    # read image specify your path 
    image = cv2.imread('1.jpg') 

    #resize image for fast detection 
    image = imutils.resize(image, 
                        width=min(400, image.shape[1])) 

    # detect people in the image
    # returns the bounding boxes for the detected objects 
    (regions, _) = hog.detectMultiScale(image, 
                                        winStride=(4, 4), 
                                        padding=(4, 4), 
                                        scale=1.05) 
     
    for (x, y, w, h) in regions:
        # display the detected boxes in the colour picture 
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2) 

    # Display the resulting frame
    cv2.imshow("Image", image) 
    cv2.waitKey(0) 
    # finally, close the window
    cv2.destroyAllWindows()


print('Write "live" or "image"')
data = input('Answer->')

if data =='live':
    webcam_live(hog)
elif data =='image':
    img_live(hog)
else:
    print('Wrong Input')