int peltPin = 3; //peltier cooler pin
int peltPin1 = 5; //second peliter cooler pin
double psuV = 10;
float c;

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
  Serial.println(readTemperature());
  OutputVoltage(0, psuV, peltPin); //test to see whether mosfet actually outputs certain voltage
  OutputVoltage(0, psuV, peltPin1);
  delay(100);
}

float readTemperature(){
  float in = analogRead(A0);
  if(in<=622)
    c = (-0.3234*in)+220.1; 
  else
    c = (-0.6932*in)+450.08;
  return c;
}
void OutputVoltage(double v, double SrcV, int pin) {
  analogWrite(pin, (v / SrcV) * 255);
}



