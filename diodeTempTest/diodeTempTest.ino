//useful link: https://drive.google.com/file/d/0B8NyMDTl1ovXYndyVnZrdDhZd1U/edit
//int diodePin = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  analogReference(INTERNAL);   
  pinMode(A0,INPUT_PULLUP);
  pinMode(A1,OUTPUT);
  digitalWrite(A1,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
delay(100);
float in = analogRead(A0);
float C = (598 - in) / 2.43 + 27.5;
Serial.print(in);
Serial.print("       ");
Serial.println(C);
}
