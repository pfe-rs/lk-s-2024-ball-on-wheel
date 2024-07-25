import cv2
import serial
import enkoder_motor
import motor
import PID
import balldetection
import time 
import matplotlib

from matplotlib import pyplot as plt
matplotlib.use('TkAgg')

zeljena_ugaona_brzina=2000
zeljena_brzina2 = 2500


duzina = 10
neko_vreme = 5
start_time = time.time()

brzina_list = []
vreme_list = []
napon_list= []
zeljena_ugaona_brzina_list = []

arduino = serial.Serial('/dev/ttyACM0',115200)

enkoder=enkoder_motor.Enkoder()
motora=motor.Motor()
loptica=balldetection.detekcija_loptice()
cap=cv2.VideoCapture(0)
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', loptica.click)
roi_x, roi_y, roi_w, roi_h = 100, 100, 200, 300


interval=0.01           #vremenski interval posle kog ce se izvrsiti fje
prethodno_vreme=time.time()
arduino.write(b'start\n')

while time.time() < start_time + duzina:
    trenutno_vreme=time.time()
    if(trenutno_vreme-prethodno_vreme>=interval):
        prethodno_vreme=trenutno_vreme

        ret, frame = cap.read()
        angle, brzina_loptice = loptica.get_polozaj(frame)
        cv2.imshow('Frame', frame)

        enkoder.citaj_podatke(arduino)
        ugaona_brzina=enkoder.odredjivanje_ugaone_brzine()
        if ugaona_brzina is not None:
            if time.time() > start_time + neko_vreme:
                zeljena_ugaona_brzina = zeljena_brzina2
            greska=PID.Geterror(zeljena_ugaona_brzina,ugaona_brzina)
            napon=PID.pid(greska,0)
            motora.salji_napon(napon,arduino) 
            sad_time = time.time() - start_time
            brzina_list.append(ugaona_brzina)
            vreme_list.append(sad_time)
            napon_list.append(napon)
            zeljena_ugaona_brzina_list.append(zeljena_ugaona_brzina)

cap.release()
cv2.destroyAllWindows()

plt.title("zavisnost brzine i napona od vremena")
plt.xlabel("vreme")
plt.ylabel("")
#plt.legend(loc='upper left', fontsize='large', title='Legend', frameon=False)
plt.plot(vreme_list,brzina_list)
plt.plot(vreme_list,napon_list)
plt.plot(vreme_list, zeljena_ugaona_brzina_list)
plt.show() 
