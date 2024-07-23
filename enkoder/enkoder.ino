#include <Encoder.h>

Encoder enc(2,3);
int speedpin=7;
int directionpin1=6;
int directionpin2=5;

long stara_pozicija=-999,nova_pozicija;
float volti=0.25*21.25;
bool f=true;
unsigned long puls;
int x;

void setup(){
  Serial.begin(115200);

  pinMode(speedpin,OUTPUT);
  pinMode(directionpin1,OUTPUT);
  pinMode(directionpin2,OUTPUT);
  analogWrite(speedpin,0);  //na motoru koji smo koristili 21.25 je otprilike 1 volt
  digitalWrite(directionpin2,HIGH);
  digitalWrite(directionpin1,LOW);
}

void loop(){
  while (!Serial.available()){
	  x = Serial.readString().toInt(); 
    analogWrite(speedpin,x);
  }
  if(f){
    Serial.println(volti);
    f=false;
}
  nova_pozicija=enc.read();
  puls=2*pulseIn(2,HIGH);
  if(nova_pozicija!=stara_pozicija){
    Serial.print(puls);
    Serial.print(",");
    Serial.println(nova_pozicija);
    stara_pozicija=nova_pozicija;
  }
}
/*long stara_pozicija = -999, nova_pozicija;
float jedinicni_ugao=(float)360/2400, volti=0.25*21.25,ugao;
unsigned long puls,puls1,puls2;

float merenje_ugla(Encoder enc){
  stara_pozicija = enc.read();
  float u=fmod(jedinicni_ugao*nova_pozicija,360.0);
  return u;
}

void reset (Encoder enc){
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset");
    enc.write(0);
  }
}

void stampaj(float x){
  Serial.print(x);
}

void loop(){ 
  nova_pozicija = enc.read();
  ugao=jedinicni_ugao*nova_pozicija;
  puls=2*pulseIn(2,HIGH);
  if (nova_pozicija != stara_pozicija) {
    Serial.println(puls);
    Serial.print(ugao);
    Serial.print(",");
    if(puls>0){
      double period = puls * 1e-6*600; // Convert microseconds to seconds
      double frequency = 1.0 / period; // Frequency in Hz
      double ugaona_brzina = frequency*60;
      Serial.println(ugaona_brzina);
    }
    stara_pozicija=nova_pozicija;
  }
  reset(enc);
}*/