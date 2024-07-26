import cv2
import numpy as np
import math
import time
from filterpy.kalman import KalmanFilter
class detekcija_loptice():
    def __init__ (self):
        self.koordinatni_pocetak = (383, 449)
        self.roi_x, self.roi_y, self.roi_w, self.roi_h = 100, 100, 200, 300
        self.kf = KalmanFilter(dim_x=2, dim_z=1)
        self.kf.x = np.array([0., 0.])  
        self.kf.F = np.array([[1., 1.],
                              [0., 1.]])  
        self.kf.H = np.array([[1., 0.]])  
        self.kf.P *= 1000.  
        self.kf.R = 5 
        self.kf.Q = np.array([[1., 0.],
                              [0., 1.]]) 
        self.pre_time = None

    def click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.koordinatni_pocetak = (x, y)

    def get_polozaj(self, frame):
        roi = frame[self.roi_y:self.roi_y+self.roi_h, self.roi_x:self.roi_x+self.roi_w]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_plava = np.array([0, 50, 30])
        upper_plava = np.array([25, 185, 225])

        mask = cv2.inRange(hsv, lower_plava, upper_plava)

        blue_only = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(blue_only, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=100, param2=30, minRadius=10, maxRadius=100)

        if circles is not None:

            circles = np.round(circles[0, :]).astype("int")
      
            for (x, y, r) in circles:
                if self.koordinatni_pocetak is not None:
                    koordinatni_pocetak_x, koordinatni_pocetak_y = self.koordinatni_pocetak

                    new_x = x - koordinatni_pocetak_x
                    new_y = koordinatni_pocetak_y - y
                    angle = math.degrees(math.atan2(new_y, new_x)) -90
                    
                    curr_time = time.time()

                    if self.pre_time is not None:
                        d_time = curr_time - self.pre_time
                        self.kf.F[0, 1] = d_time  
                        self.kf.predict()
                        self.kf.update(angle)
                        brzina_loptice = self.kf.x[1]
                    else:
                        brzina_loptice = 0

                    self.pre_time = curr_time
                    
                    # cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                    # cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
                    
                    # cv2.putText(frame, f"Angle: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    # cv2.putText(frame, f"Angular Speed: {brzina_loptice:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                   
                    return angle, brzina_loptice
        
        return None, None


if __name__ == "__main__":

    bd = detekcija_loptice()
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', bd.click)

    roi_x, roi_y, roi_w, roi_h = 100, 100, 200, 300


    while True:
        ret, frame = cap.read()

        if not ret:
            break

        angle, brzina_loptice = bd.get_polozaj(frame)
        if angle is not None:
            print(angle, brzina_loptice)
        
        # Display the frame
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
