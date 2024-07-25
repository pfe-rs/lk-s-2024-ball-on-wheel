#include <Encoder.h>

Encoder enc(2,3);
int speedpin=9;
int directionpin1=6;
int directionpin2=7;
  
long stara_pozicija=-999,nova_pozicija;
float volti=0.25*21.25;
bool f=true;
unsigned long puls, start_time=0;
int x,pwmValue;

void setup(){
  Serial.begin(115200);

  pinMode(speedpin,OUTPUT);
  pinMode(directionpin1,OUTPUT);
  pinMode(directionpin2,OUTPUT);
  //analogWrite(speedpin,150);  //na motoru koji smo koristili 21.25 je otprilike 1 volt
  //digitalWrite(directionpin2,HIGH);
  //digitalWrite(directionpin1,LOW);

  while (!Serial.available()) {
    // Wait for start signal
  }
  if (Serial.readString() == "start\n") {
    start_time = millis();
  }
}

void loop(){
  if (Serial.available()) {
    int newPwmValue = Serial.parseInt();  // Read the PWM value sent from Python
    if (newPwmValue > -255 && newPwmValue <= 255 && newPwmValue!=0) {
      pwmValue = newPwmValue;  // Update PWM value only if valid
    }
  }

  if (pwmValue > 0){
    analogWrite(speedpin, pwmValue); // Set the motor speed
    digitalWrite(directionpin2,HIGH);
    digitalWrite(directionpin1,LOW);
  }
  else{
    analogWrite(speedpin, -pwmValue); // Set the motor speed
    digitalWrite(directionpin2,LOW);
    digitalWrite(directionpin1,HIGH);
  }

  /*if(f){
    Serial.println(volti);
    f=false;
  }*/
  nova_pozicija=enc.read();
  puls=2*pulseIn(2,HIGH);
  Serial.print(puls);
  Serial.print(",");
  Serial.println(nova_pozicija); 
  //  stara_pozicija=nova_pozicija;
}
