
import serial
import enkoder_motor
import motor
import PID
import time 
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')

zeljena_ugaona_brzina=210
zeljena_brzina2 = 350


duzina = 40
neko_vreme = 20
start_time = time.time()

brzina_list = []
vreme_list = []
napon_list= []
zeljena_ugaona_brzina_list = []

arduino = serial.Serial('/dev/ttyACM0',115200)

enkoder=enkoder_motor.Enkoder()
motor=motor.Motor()
#interval=0.01           #vremenski interval posle kog ce se izvrsiti fja
#prethodno_vreme=time.time()

while time.time() < start_time + duzina:
    #trenutno_vreme=time.time()
    #if(trenutno_vreme-prethodno_vreme>=interval):
      #  prethodno_vreme=trenutno_vreme
        enkoder.citaj_podatke(arduino)
        ugaona_brzina=enkoder.odredjivanje_ugaone_brzine()
        if ugaona_brzina is not None:
            if time.time() > start_time + neko_vreme:
                zeljena_ugaona_brzina = zeljena_brzina2
            greska=PID.Geterror(zeljena_ugaona_brzina,ugaona_brzina)
            napon=PID.pid(greska,0)
            motor.salji_napon(napon,arduino)  

            sad_time = time.time() - start_time
            brzina_list.append(ugaona_brzina)
            vreme_list.append(sad_time)
            napon_list.append(napon)
            zeljena_ugaona_brzina_list.append(zeljena_ugaona_brzina)



plt.plot(vreme_list,brzina_list)
plt.plot(vreme_list,napon_list)
plt.plot(vreme_list, zeljena_ugaona_brzina_list)
plt.show() 
