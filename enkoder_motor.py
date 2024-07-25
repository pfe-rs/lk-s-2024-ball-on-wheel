import serial
import time
 
arduino = serial.Serial('/dev/ttyACM0',115200)
jedinicni_ugao=360/2400
class Enkoder:
    def odredjivanje_ugla(self):
        self.ugao=int(jedinicni_ugao*self.poz)%360
        return self.ugao
    def odredjivanje_ugaone_brzine(self):
        if(self.puls>0):
            self.period = self.puls * 1e-6*600
            self.frequency = 1.0 / self.period
            self.ugaona_brzina = self.frequency*360
            return self.ugaona_brzina
    def citaj_podatke(self, arduino):
        dataPacket=arduino.readline()
        dataPacket=str(dataPacket, 'utf-8')
        dataPacket=dataPacket.strip('\r\n')
        splitPacket=dataPacket.split(",")
        if len(splitPacket) != 2:
            print("nema 2broja")
            return
        self.puls=int(splitPacket[0])  
        self.poz=int(splitPacket[1])
    def citaj_napon(self,arduino):
        self.napon=arduino.readline()
        self.napon=str(self.napon, 'utf-8')
        self.napon=self.napon.strip('\r\n')
        return self.napon

if __name__=="__main__":
    time.sleep(1)

    enkoder=Enkoder()    
    napon=enkoder.citaj_napon(arduino)
    print("napon= ",napon)

    while True:
        while (arduino.inWaiting()==0):
            pass
        enkoder.citaj_podatke(arduino)
        ugao=enkoder.odredjivanje_ugla()
        ugaona_brzina=enkoder.odredjivanje_ugaone_brzine()
        print("ugao= ",enkoder.odredjivanje_ugla(), "ugaona brzina= ", enkoder.odredjivanje_ugaone_brzine())
    
