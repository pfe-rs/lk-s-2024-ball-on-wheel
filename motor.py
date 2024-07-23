import serial
import time

arduino = serial.Serial('/dev/ttyACM0',115200)

class Motor:
    def __init__(self,napon):
        self.napon=napon
    def salji_napon(self,arduino):
        if 0 <= self.napon <= 255:
            arduino.write(f"{self.napon}\n".encode())

time.sleep(1)

while True:    
    print("Uneti napon")
    napon=int(input())
    motor=Motor(napon)
    motor.salji_napon(arduino)
