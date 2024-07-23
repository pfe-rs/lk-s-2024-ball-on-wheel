import serial
import time

arduino = serial.Serial('/dev/ttyACM1',115200)

class Motor:
    def salji_napon(self,napon,arduino):
        if 0 <= napon <= 255:
            arduino.write(f"{napon}\n".encode())
            time.sleep(0.1)  # Allow some time for the Arduino to process
            while arduino.in_waiting > 0:
                arduino.readline()  # Clear the buffer

time.sleep(1)

while True:    
    print("Uneti napon")
    napon=int(input())
    motor=Motor()
    motor.salji_napon(napon,arduino)
