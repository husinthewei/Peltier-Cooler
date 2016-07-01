int targetTemp = -2; //setting temporary target temp
//PID stuff
int Actual = 0;
int Error = 0;
int Integral = 0;
int Last = 0;
int IntThresh = targetTemp + 5;
double kP = 8;
double kI = 0.3;
double kD = 0.3;
int ScaleFactor = 1;
//
const int len = 10;
double prevTemps[len];
double averageTemp;
//
int peltPin = 3; //peltier cooler pin (smaller peltier)
int peltPin1 = 6; //second peliter cooler pin (big peltier)
//
double psuV = 12;
//
float c;
//
void setup() {
  pinMode(peltPin, OUTPUT);
  pinMode(peltPin1, OUTPUT);
  Serial.begin(9600);
  analogReference(INTERNAL);
  pinMode(A0, INPUT_PULLUP);
  //pinMode(A0, INPUT);
  pinMode(A1, OUTPUT);
  digitalWrite(A1, LOW);
  Last = analogRead(A0);

  double temp = readTemperature();
  for(int i = 0; i < len; i++)
    prevTemps[i] = temp;
}

void loop() {
  //double currentTemp = readTemperature();
  //recordTemp(currentTemp);
  //int drive = getPID();
  int drive = 0;
  //analogWrite(peltPin, 30);     // smaller & orange 
  //analogWrite(peltPin1, 30);//bigger & gray

  OutputVoltage(5, psuV, peltPin); // smaller & orange (max 8.6V, and 6A) Max 9.5
  OutputVoltage(5, psuV, peltPin1);//bigger & gray (max 14.5V, and 14.7A)

  double raw = analogRead(A0);
  Serial.print(raw);
  
  Serial.print("    T: ");
  //Serial.print(currentTemp);

  recordTemp(raw);
  Serial.print("   TAve: ");
  Serial.print(getAve());
  
  Serial.print("   Dr:");
  Serial.println(drive);
  
  delay(100);
}

int getPID(){
  Actual = readTemperature();
  Error = Actual - targetTemp;

  if(abs(Error)<IntThresh){
    Integral = Integral + Error;
  }
  else{
    Integral = 0;
  }
  
  int P = Error * kP;
  int I = Integral * kI;
  int D = (Last-Actual)*kD;
  int Drive = P+I+D;
  Serial.print("P: ");
  Serial.print(P);
  Serial.print("    I:");
  Serial.print(I);
  Serial.print("    D:");
  Serial.print(D);
  Serial.print("    ");
  Drive = Drive*ScaleFactor;
  if(abs(Drive)>255){
    Drive = 255;
  }
  return Drive;
}

void recordTemp(double temp){
  for(int i = len-1; i > 0 ; i--){
    prevTemps[i] = prevTemps[i-1];
  }
  prevTemps[0] = temp;
}

double getAve(){
  double sum = 0;
  for(int i = 0; i < len; i++)
    sum += prevTemps[i];

  return (double)(sum / len); 
}

double readTemperature(){
  double in = analogRead(A0);
  if(in<=622)
    c = (-0.3234*in)+220.1; 
  else
    c = (-0.6932*in)+450.08;
  return c;
}
void OutputVoltage(double v, double SrcV, int pin) {
  analogWrite(pin, (v / SrcV) * 255);
}
