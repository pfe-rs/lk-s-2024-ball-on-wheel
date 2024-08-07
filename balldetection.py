import cv2
import numpy as np
import math


class detekcija_loptice():
    def __init__ (self):
        self.koordinatni_pocetak = (0, 0)
        self.roi_x, self.roi_y, self.roi_w, self.roi_h = 100, 100, 200, 300

    def click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.koordinatni_pocetak = (x, y)

    def get_polozaj(self, frame):
        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

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
                    angle = math.degrees(math.atan2(new_y, new_x))
                    
                    return angle


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

        angle = bd.get_polozaj(frame)
        print(angle)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

#захвалност никлоли најићу!!
