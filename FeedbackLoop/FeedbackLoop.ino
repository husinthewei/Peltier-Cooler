int tempPin = 2;
double ratio = 10; //temporary ratio for input to degrees celsius
//
int targetTemp = -10;

int peltPin = 3;
//
double psuV = 12;
//
void setup() {
  pinMode(peltPin, OUTPUT);
  pinMode(tempPin, INPUT);
}

void loop() {
  double currentTemp = getTemp();
  double diff = currentTemp - targetTemp;

  double targV = constrain(((diff <= 0) ? 0 : diff), 0, 12); //
  
  OutputVoltage(targV, psuV, peltPin);

  delay(50);
}

void OutputVoltage(double v, double SrcV, int pin){
  analogWrite(pin, (v/SrcV) * 255);
}

double getTemp(){
  //I don't currently know which temperature sensor we are using
  //Temporarily using just analogRead to "get temperature"
  return analogRead(tempPin) * ratio;
}

