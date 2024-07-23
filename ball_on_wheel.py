import serial
import time
import enkoder_motor
import motor
import PID

zeljena_ugaona_brzina=20

arduino = serial.Serial('/dev/ttyACM0',115200)

while True:
    enkoder=enkoder_motor.Enkoder()
    enkoder.citaj_podatke(arduino)
    ugaona_brzina=enkoder.odredjivanje_ugaone_brzine()
    greska=PID.Geterror(zeljena_ugaona_brzina,ugaona_brzina)
    napon=PID.pid(greska,0)
    motor=motor.Motor(napon)
    motor.salji_napon(arduino)