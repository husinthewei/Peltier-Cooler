//useful link: https://drive.google.com/file/d/0B8NyMDTl1ovXYndyVnZrdDhZd1U/edit
//int diodePin = 0;

double base = 1013;void setup() {
  pinMode(A0,INPUT_PULLUP);
  pinMode(A1,OUTPUT);
  digitalWrite(A1,LOW);
  Serial.begin(9600);
}

void loop() {
 double in = analogRead(A0);
 Serial.print(in);
 Serial.print("    ");
 double V = (((1013 - in)/1023) * 5);
 double C = 27 + (V/0.02);
 Serial.print(C);
 Serial.print("    ");
 double F = (1.8)*C + 32;
 Serial.println(F);
 
 delay(100);
}
