import cv2
import numpy as np
import math

def get_polozaj_loptice():
    global koordinatni_pocetak
    koordinatni_pocetak = (0, 0)

    def click(event, x, y, flags, param):
        global koordinatni_pocetak
        if event == cv2.EVENT_LBUTTONDOWN:
            koordinatni_pocetak = (x, y)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', click)

    roi_x, roi_y, roi_w, roi_h = 100, 100, 200, 300

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break

        # isecanje frame-a tako da ostane vrh tocka kako bi se sto vise izbegle nezeljene detekcije
        roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_plava = np.array([0, 50, 30])
        upper_plava = np.array([25, 185, 225])

        # ostavljanje samo piksela koji su boje loptice koja se koristi
        mask = cv2.inRange(hsv, lower_plava, upper_plava)

        blue_only = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(blue_only, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # detekcija krugova
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=100, param2=30, minRadius=10, maxRadius=100)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            
            if koordinatni_pocetak is not None:
                koordinatni_pocetak_x, koordinatni_pocetak_y = koordinatni_pocetak

                new_x = x - koordinatni_pocetak_x
                new_y = koordinatni_pocetak_y - y
                angle = math.degrees(math.atan2(new_y, new_x))
                
                cv2.putText(frame, f"Angle: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                merenje = np.array([[np.float32(x)], [np.float32(y)]])
        
            cv2.line(frame, (koordinatni_pocetak_x, 0), (koordinatni_pocetak_x, frame.shape[0]), (0, 0, 255), 2)
            cv2.line(frame, (0, koordinatni_pocetak_y), (frame.shape[1], koordinatni_pocetak_y), (0, 255, 0), 2)

        frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w] = roi
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return angle
