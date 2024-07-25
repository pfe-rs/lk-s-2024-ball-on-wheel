import serial
import time

arduino = serial.Serial('/dev/ttyACM0',115200)

class Motor:
    @staticmethod
    def salji_napon(napon,arduino):
        s = time.time()
        napon=max(-254,min(255,napon))
        arduino.write(f"{napon}\n".encode())
        while arduino.in_waiting > 0:
            arduino.readline()  # Clear the buffer


if __name__=="__main__":
    time.sleep(1)

    while True:    
        print("Uneti napon")
        napon=int(input())
        motor=Motor()
        motor.salji_napon(napon,arduino)
