import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


cap = cv2.VideoCapture(0)  


#kalmanov filter za pracenje loptice
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

prev_x, prev_y = None, None

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

     
    lower_plava = np.array([100, 150, 50]) #podesava u zavisnosti od boje loptice koja se koristi
    upper_plava = np.array([140, 255, 255])


    #ostavlja samo opseg boja u kojima se nalazi loptica radi preci
    mask = cv2.inRange(hsv, lower_plava, upper_plava)

    blue_only = cv2.bitwise_and(frame, frame, mask=mask)
    
    gray = cv2.cvtColor(blue_only, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=100, param2=30, minRadius=10, maxRadius=100)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    
        frame_centar_x = frame.shape[1] // 2
        frame_centar_y = frame.shape[0] // 2

        
        #racuna poziciju 
        new_x = x - frame_centar_x
        new_y = frame.shape[0] - y 
        angle = math.degrees(math.atan2(new_y, new_x))
        
        cv2.putText(frame, f"Angle: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        merenje = np.array([[np.float32(x)], [np.float32(y)]])
        kalman.correct(merenje)
        prediction = kalman.predict()
        

        #tracking
        pred_x, pred_y = prediction[0], prediction[1]
        vel_x, vel_y = prediction[2], prediction[3]

        print(vel_x, vel_y)

    frame_centar_x = frame.shape[1] // 2
    cv2.line(frame, (frame_centar_x, 0), (frame_centar_x, frame.shape[0]), (0, 0, 255), 2)

    cv2.line(frame, (0, frame.shape[0]), (frame.shape[1], frame.shape[0]), (0, 255, 0), 2)

    cv2.imshow('', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
