import cv2
import numpy as np
import math

koordinatni_pocetak = (0, 0)

#da se koordinatni pocetak postavi tamo gde se klikne (treba biti centar tocka)
def click(event, x, y, flags, param):
    global koordinatni_pocetak
    if event == cv2.EVENT_LBUTTONDOWN:
        koordinatni_pocetak = (x, y)

cap = cv2.VideoCapture(0)
cv2.namedWindow('ROI')
cv2.setMouseCallback('ROI', click)

#za pracenje loptice
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

# Definisanje regiona od interesa (ROI)
roi_y, roi_x, roi_w, roi_h = 80, 126, 470, 260

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Isjecanje ROI iz frejma
    roi = frame[roi_x:roi_x+roi_h, roi_y:roi_y+roi_w]
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_plava = np.array([0, 50, 30])
    upper_plava = np.array([25, 185, 225])

    mask = cv2.inRange(hsv, lower_plava, upper_plava)
    
    blue_only = cv2.bitwise_and(roi, roi, mask=mask)
    gray = cv2.cvtColor(blue_only, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=100, param2=30, minRadius=10, maxRadius=100)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(roi, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(roi, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
        if koordinatni_pocetak is not None:
            koordinatni_pocetak_x, koordinatni_pocetak_y = koordinatni_pocetak

            new_x = x + roi_x - koordinatni_pocetak_x
            new_y = koordinatni_pocetak_y - (y + roi_y)
            angle = math.degrees(math.atan2(new_y, new_x))
            
            cv2.putText(roi, f"Angle: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            merenje = np.array([[np.float32(x + roi_x)], [np.float32(y + roi_y)]])
            kalman.correct(merenje)
            prediction = kalman.predict()
            
            pred_x, pred_y = prediction[0], prediction[1]

            vel_x, vel_y = prediction[2], prediction[3]

            print(vel_x, vel_y)
        
        cv2.line(roi, (koordinatni_pocetak_x - roi_x, 0), (koordinatni_pocetak_x - roi_x, roi.shape[0]), (0, 0, 255), 2)
        cv2.line(roi, (0, koordinatni_pocetak_y - roi_y), (roi.shape[1], koordinatni_pocetak_y - roi_y), (0, 255, 0), 2)

    # Prikazivanje samo ROI
    cv2.imshow('ROI', roi)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
