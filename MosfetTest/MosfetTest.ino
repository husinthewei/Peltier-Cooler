int peltPin = 3; //peltier cooler pin
double psuV = 12;
void setup() {
  pinMode(peltPin, OUTPUT);
}

void loop() {
  OutputVoltage(5,psuV,peltPin); //test to see whether mosfet actually outputs 5v
  delay(100);
}

void OutputVoltage(double v, double SrcV, int pin){
  analogWrite(pin, (v/SrcV) * 255);
}

