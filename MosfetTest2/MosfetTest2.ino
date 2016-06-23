int peltPin = 3; //peltier cooler pin
int peltPin1 = 5; //second peliter cooler pin
double psuV = 8;
void setup() {
  pinMode(peltPin, OUTPUT);
  pinMode(peltPin1, OUTPUT);
  Serial.begin(9600);
  analogReference(INTERNAL);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, OUTPUT);
  digitalWrite(A1, LOW);
}

void loop() {
  OutputVoltage(5, psuV, peltPin); //test to see whether mosfet actually outputs certain voltage
  OutputVoltage(5, psuV, peltPin1);
  delay(100);


  float in = analogRead(A0);
  float C = (598 - in) / 2.43 + 27.5;
  Serial.print(in);
  Serial.print("       ");
  Serial.println(C);
}

void OutputVoltage(double v, double SrcV, int pin) {
  analogWrite(pin, (v / SrcV) * 255);
}



