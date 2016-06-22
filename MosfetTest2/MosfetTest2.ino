int peltPin = 3; //peltier cooler pin
int peltPin1 = 5; //second peliter cooler pin
double psuV = 8;
void setup() {
  pinMode(peltPin, OUTPUT);
  pinMode(peltPin1, OUTPUT);
}

void loop() {
  OutputVoltage(6,psuV,peltPin); //test to see whether mosfet actually outputs certain voltage
  OutputVoltage(8,psuV,peltPin1); 
  delay(100);
}

void OutputVoltage(double v, double SrcV, int pin){
  analogWrite(pin, (v/SrcV) * 255);
}



