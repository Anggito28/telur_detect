#include <Servo.h>

Servo servo;
Servo servo1;
byte ldr = A0;
byte led = 13;
int nilai = 0 ;


void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  servo.attach(9);
  servo1.attach(10);
}

void loop() {
  // put your main code here, to run repeatedly:
  nilai = analogRead(ldr);
  Serial.print("Nilai LDR: ");
  Serial.println(nilai);

  if (nilai >= 400) {
    digitalWrite(led, HIGH);
    servo1.write(110);
    delay(1000);
  }else {
    digitalWrite(led, LOW);
  }
}
