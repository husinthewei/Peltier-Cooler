int targetTemp = -2; //setting temporary target te,p

int peltPin = 3; //peltier cooler pin
int peltPin1 = 5; //second peliter cooler pin
//
double psuV = 10;
//
float c;
//
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

  //new feedback algorithm:
  //Use equation to find ideal voltage for certain temperature. 
  //ex: use from graphs during diode testing
  //loop- 
  //1. if temp is (>2C?) above targer, peltier max
  //2. if temp is (>2C?) below target, peltier 0.4
  //3. if temp is +-2 from target, peltier at ideal
  
  double currentTemp = readTemperature();
  double diff = currentTemp - targetTemp;

  double targV = constrain(((diff <= 0) ? 0 : diff + 4), 6, psuV); //
  OutputVoltage(targV, psuV, peltPin);
  OutputVoltage(targV, psuV, peltPin1);

  Serial.println(currentTemp);
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

