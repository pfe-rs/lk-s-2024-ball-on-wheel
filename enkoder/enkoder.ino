#include <Encoder.h>

Encoder Ludi(2,3);
int speedpin=7;
int directionpin1=6;
int directionpin2=5;

long pozicijaLudi  = -999, noviLudi;
int start=0, f=1;
float ugao, jedinicni_ugao=(float)360/2400,ugaona_brzina, volti=6*21.25;

void setup() {
  Serial.begin(115200);

  pinMode(speedpin,OUTPUT);
  pinMode(directionpin1,OUTPUT);x 
  pinMode(directionpin2,OUTPUT);
  analogWrite(speedpin,127);  //na motoru koji smo koristili 21.25 je otprilike 1 volt
  digitalWrite(directionpin2,HIGH);
  digitalWrite(directionpin1,LOW);
}

void reset (Encoder Ludi){
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset");
    Ludi.write(0);
  }
}

void stampaj(float x){
  Serial.print(x);
}

float merenje_ugla(Encoder Ludi){
  noviLudi = Ludi.read();
  float u=fmod(jedinicni_ugao*noviLudi,360.0);
  return u;
}

float merenje_ugaone_brzine(int start){
    int tr= micros();
    int vreme=tr-start;
    float ub=(float)abs(noviLudi*jedinicni_ugao-pozicijaLudi*jedinicni_ugao)/vreme*1000000;
    start=tr;
    return ub;
}

void loop() {
  if (f){
    stampaj(volti/21.25);
    f--;
  }
  ugao=merenje_ugla(Ludi);
  if (noviLudi != pozicijaLudi) {
    //stampaj(ugao);
    //Serial.print(" , ");
    ugaona_brzina=merenje_ugaone_brzine(start);
    stampaj(ugaona_brzina);
    Serial.println();
    pozicijaLudi = noviLudi;
  }
  reset(Ludi);
  Serial.flush();
  //delay(200);
}

