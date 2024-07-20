import serial
import time
 
arduino = serial.Serial('/dev/ttyACM0',9600)

time.sleep(1)

while True:
    while (arduino.inWaiting()==0):
        pass

    dataPacket=arduino.readline()
    dataPacket=str(dataPacket, 'utf-8')
    dataPacket=dataPacket.strip('\r\n')
    print(dataPacket)
