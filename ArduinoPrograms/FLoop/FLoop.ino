//PID stuff: Values for PID calculation
//PID is not being currently used and may not be used in the final product
int targetTemp = -10; 
double Actual = 0; 
double Error = 0;
double Integral = 0;
double Last = 0;
int IntThresh = targetTemp + 12;
double kP = 20;   
double kI = 0.1; 
double kD = 0.6; 
double ScaleFactor = 1;
int drive = 0; //Current drive value is 0, so no PID is used. If using PID, comment this line out
//Average calculation variables.
//Len 10 means over 1 second
const int len = 10; 
double prevTemps[len]; 
double averageTemp;
//If there are enough "outliers"/"bad readings", maybe they are actually correct. 
//If there are enough consecutive bad readings, then trust them.
int badReadings = 0;                   
int peltPin = 3;   //peltier cooler pin (smaller peltier touching board)
int peltPin1 = 9; //second peliter cooler pin (big peltier touching heatsink)
//
int outV = 12; 
double psuV = 12; 
//
float c;
//mechanism to turn peltiers off if the temp gets too hot (e.g. fan turns off or some failure)
int changeCount = 0;          //make sure at least 30 readings before switching states
double onThresh = -8;        //temperature threshold to turn on this mechanism. (on state)
double badThresh = 0;       //temperature threshold to signal that something bad is happening(bad state)
boolean reachedOn = false; //signals on state
int LEDPin = 10;          //LED that turns on during on state. Off signals a problem.
//Code to slowly ramp the MOSFET's on
  boolean MosfetsOn = false;
//
void setup() {
  pinMode(peltPin, OUTPUT); 
  pinMode(peltPin1, OUTPUT);
  Serial.begin(9600); 
  analogReference(INTERNAL); 
  pinMode(A0, INPUT_PULLUP); 
  pinMode(A1, OUTPUT); 
  pinMode(LEDPin, OUTPUT); 
  digitalWrite(A1, LOW); 
  digitalWrite(LEDPin, LOW);
  Last = readTemperature(); 

  //fills temperature array for initial average calculation
  double temp = readTemperature(); 
  for(int i = 0; i < len; i++)
    prevTemps[i] = temp;
}

void loop() { 
  double currentTemp = readTemperature(); 
  double ave = getAve(); 
  
  if(badReading(currentTemp)) 
    currentTemp = getAve();                   //using average if current reading is "outlier"
  else
    recordTemp(currentTemp);                            
    
  //*Uncomment below part to do PID stuff
  //int drive = getPID();                   //calculates what drive value (out of 255) to use for PWM. Proportional to duty cycle (i.e. 51/255 = 0.2, meaning 20% duty cycle)
  //analogWrite(peltPin, drive);            //writes drive value to small Peltier
  //analogWrite(peltPin1, drive);           //writes drive value to large Peltier

  //testing serial output from the python
  String inMsg = Serial.readString();
  if(inMsg == "Mosfets_On"){
    MosfetsOn = HIGH;
  }
  if(inMsg == "Mosfets_Off"){
    digitalWrite(LEDPin, LOW);
    MosfetsOn = LOW;
    drive = 0;
  }
  
  if(MosfetsOn){
    digitalWrite(LEDPin, HIGH);
    drive = constrain(drive + 1, 0, 255);
  }
    
  //OutputVoltage(outV, psuV, peltPin);       // smaller & orange (max 14.4V and 6.4A). TEC1-12706
  analogWrite(peltPin, drive); 
  analogWrite(peltPin1, drive); 
  checkSafe(ave);                           //Checking safety mechanism

  Serial.print(currentTemp); //prints the target temp. This is what the python script cares about


  
  //The python script ignores all of this.
  double raw = analogRead(A0); 
  Serial.print("    Raw: ");
  Serial.print(raw); 
  
  Serial.print("    T: ");
  Serial.print(currentTemp); 
  
  Serial.print("    Tf: ");
  Serial.print(getF(currentTemp)); 
  
  Serial.print("   TAve: ");
  Serial.print(ave); 
  
  Serial.print("   Dr:");
  Serial.println(drive); 
  
  delay(100); 
}




/*FUNCTIONS:
 * checkSafe(ave); Safety mechanism to turn off Peltier's if system starts getting hot
 * getPid(); calculates PID value and returns it. Can be used like:  int drive = getPID(); 
 * badReading(temp); Checks whether temp is an outlier (e.g. bad diode reading) and returns the result
 * recordTemp(temp); Takes the parameter (temp) and stores it for average calculation. Can be used like:  recordTemp(currentTemp);
 * getAve(); Calculates the average. Can be used like: double average = getAve()
 * readTemperature(); Calculates temperature form raw input and returns it. Can be used like:  double currentTemp = readTemperature();
 * getF(C); Converts a celsius temperature into fahrenheit and returns it
 * OutputVoltage(v, SrcV, pin); Calculates duty cycle to use to reach v from the SrcV (source voltage) and outputs it to the pin. Can be used like: OutputVoltage(3, psuV, peltPin);
 */

void checkSafe(double ave){
  if(reachedOn == false && ave < onThresh)       //increase the counter to reach the on state
    changeCount +=1;
    
  if(changeCount >= 30 && reachedOn == false){  //if 30 counts met, turns the mechanism on (on state)
    changeCount = 0;
    reachedOn = true;
    //digitalWrite(LEDPin, HIGH);
  }

  if(reachedOn == true && ave >= badThresh)     //increase the counter to reach the "problem state". Must be in on state
    changeCount +=1;

  if(reachedOn == true && ave < badThresh)     //Makes it so the counts must be consecutive.
    changeCount = 0;
    
  if(changeCount >= 30 && reachedOn == true){  //if 30 counts met, the mechanism reports a problem and turns off the Peltiers
    changeCount = 0;
    outV = 0;
    for(int i = 0; i < 3; i++)                //Signaling Python to email
      Serial.println("failure");
    //digitalWrite(LEDPin, LOW);
  }
}

//function that calculates and returns PID value.  
int getPID(){ 
  Actual = readTemperature();
  Error = Actual - targetTemp;

  if(abs(Error)<IntThresh && abs(Last-Actual) < 4){   //prevents spikes
    Integral = Integral + Error;
  }
  else{
    Integral = 0;
  }
  
  double P = Error * kP;
  double I = Integral * kI;
  double D = (Last-Actual)*kD;
  double Drive = P+I+D;
  Last = Actual;
  Serial.print("P: ");
  Serial.print(P);
  Serial.print("    I:");
  Serial.print(I);
  Serial.print("    D:");
  Serial.print(D);
  Serial.print("    ");
  Drive = Drive*ScaleFactor;
  if(Drive>255){
    Drive = 255;
  }
  if(Drive<0){
    Drive = 0;
  }
  return Drive;
}

//To ignore spikes or misreadings, this will only allow readings 3 degrees from the average
//If there are enough bad readings, they might actually be right. 
//If # of badReadings high enough, will now trust these "bad" readings
boolean badReading(double temp){
  double ave = getAve();
  if(abs(temp-ave) >=3 && badReadings < 5){
    badReadings++;
    return true;
  }
  else{
    badReadings = 0;  
    return false;
  }
}

//records temperature for calculating average
void recordTemp(double temp){ 
  for(int i = len-1; i > 0 ; i--){
    prevTemps[i] = prevTemps[i-1];
  }
  prevTemps[0] = temp;
}

//calculates and returns average
double getAve(){ 
  double sum = 0;
  for(int i = 0; i < len; i++)
    sum += prevTemps[i];
  return (double)(sum / len); 
}

//calculates and returns temperature. 
double readTemperature(){ 
  double in = analogRead(A0); 
  c = (-0.5584*in) + 357.63;
  return c;
}

//converts C to F
double getF(double C){ 
  return (9*(C/5) + 32);
}

//uses PWM to output voltage using calculated duty cycle. Ex: v = 2.4, SrcV = 12. Uses a 20% duty cycle
void OutputVoltage(double v, double SrcV, int pin) { 
  analogWrite(pin, (v / SrcV) * 255);
}
