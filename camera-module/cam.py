import cv2
import time
import datetime

capture = cv2.VideoCapture(0) # Instantiating new capture device to be read

# Instantiating face and body detection modules
face_cascade = cv2.CascadeClassifier("classifiers/haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier("classifiers/haarcascade_fullbody.xml")
car_cascade = cv2.CascadeClassifier("classifiers/cars.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(capture.get(3)), int(capture.get(4))) # capture.get(3) = width, capture.get(4) = height (returns a float)
fourcc = cv2.VideoWriter_fourcc(*"mp4v") # Saved video format (asterick decomposes string and passes as 4 params)

while True:
    _, frame = capture.read() # Capture the img in a frame

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale img
    faces = face_cascade.detectMultiScale(grayscale, 1.3, 5) # Returns list of faces present in the camera
                                                             # Params: (1. grayscale img, 2. scale factor, 3. min # of neighbors)
                                                             # param2 determines speed & accuracy of the program.
                                                             #      Lower = more accuracy, Higher = faster (Best between 1.1 - 1.5) 
                                                             # param3 determines min # of faces to detect to consider it a face
                                                             #      (Best between 3 - 6) 
                                                             #      Lower = more faces detectedHigher = less faces detected
    bodies = body_cascade.detectMultiScale(grayscale, 1.3, 5) # Returns list of bodies present in the camera 
                                                              # Params work same as face cascade but with bodies

    """ if (len(faces) + len(bodies) > 0): # If a face or body is detected
        if detection: # Check if already detecting, don't stop recording while we detect
            timer_started = False
        else: # Start new recording
            detection = True
            current_time = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"recordings/{current_time}.mp4", fourcc, 20, frame_size) # Output stream
                                                                                            # Params: (1. filename, 
                                                                                            # 2. four character code, 
                                                                                            # 3. framerate, 4. frame size)
            print("Recording in progess...")
    elif detection: # Check f a body or face wasn't detected, but was detected previously, start ending timer
        if timer_started: # Check the timer has already started
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION: # Check if timer is passed its 
                                                                                          # recording halt buffer, if so, stop
                detection = False
                timer_started = False
                out.release()
                print("Ended recording")
        else: # Start the recording halt buffer
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame) """

    # Draw face boundaries on image
    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x,y), (x + width, y + height), (0, 0, 255), 3) # Params: (1. img to draw, 2. top left of rectangle
                                                                               # 3. bottom right of rectangle
                                                                               # 4. rectangle color (BGR) 5. line thickness)
    # Draw body boundaries on image
    # for (x, y, width, height) in bodies:
    #     cv2.rectangle(frame, (x,y), (x + width, y + height), (0, 0, 255), 3)

    cv2.imshow("Security Camera", frame) # Show the image

    # Exit out of the camera
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
#out.release()
capture.release()
cv2.destroyAllWindows()
