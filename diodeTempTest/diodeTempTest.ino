//useful link: https://drive.google.com/file/d/0B8NyMDTl1ovXYndyVnZrdDhZd1U/edit
//int diodePin = 0;
void setup() {
  pinMode(A0,INPUT_PULLUP);
  pinMode(A1,OUTPUT);
  digitalWrite(A1,LOW);
  Serial.begin(9600);
}

void loop() {
 Serial.println(analogRead(A0));
 delay(100);
}
