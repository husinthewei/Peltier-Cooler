/*
 * Commented version of the feedback loop
 * 
 * 
 * Code Execution order:
 * 1. setup()
 * 2. loop()
 * Then loops the code inside of loop indefinitely
 * 
 * Some basic arduino function:
 * Serial.print(); Prints on the same line. If printing text, use quotations. If printing variable, do not use quotations
 * Serial.println(); Prints on the same line, then creates new one. Same rules as Serial.print();
 * 
 * 
 * Note: If something is unclear, definitely email (wei4wei@gmail.com) or facebook message me.
 */

 
//PID stuff: Values for PID calculation
int targetTemp = -10; //setting target temp. Attempts to stay at this. PID may not be used in the final product.
double Actual = 0; 
double Error = 0;
double Integral = 0;
double Last = 0;
int IntThresh = targetTemp + 12;
double kP = 20;   //P coefficient: modify if your are calibrating PID 
double kI = 0.1; //Integral coefficient
double kD = 0.6; //Derivative coefficient
double ScaleFactor = 1;
//
const int len = 10; //How many samples to use for the average. The time the sample is over is the number of samples divided by 10 (i.e. 10 samples / 10 = 1 second)
double prevTemps[len]; //array to store temperatures for average calculation
double averageTemp;
//
int badReadings = 0; //If there are enough "outliers"/"bad readings", maybe they are actually correct. If there are enough consecutive
                     //bad readings, then trust them.
//
int tempThresh = targetTemp + 2; //Threshold to turn LED on
int LEDPin = 10; //LED on signals that the system is running well (below or near target temp)
//
int peltPin = 3; //peltier cooler pin (smaller peltier on board)
int peltPin1 = 9; //second peliter cooler pin (big peltier connected to heatsink)
//
int outV = 12; //What voltage to output. Divided by psuV for pwm output. psuV is the max outV.
double psuV = 12; //Value used for calculation in OutputVoltage();
//
float c;
//mechanism to turn peltiers off if the temp gets too hot (e.g. fan turns off or some failure)
int changeCount = 0; //make sure at least 30 readings before switching states
double onThresh = -8; //temperature threshold to turn on this mechanism. (on state)
double badThresh = 0; //temperature threshold to signal that something bad is happening(bad state)
boolean reachedOn = false; //signals on state
//
void setup() {
  pinMode(peltPin, OUTPUT); 
  pinMode(peltPin1, OUTPUT);
  Serial.begin(9600); 
  analogReference(INTERNAL); //Brings the reference voltage to 1.1v so that diode has more resolution.
  pinMode(A0, INPUT_PULLUP); //Declares as input and uses the internal 10k resistor as pullup. This is the input pin of the diode (analog pin 0)
  pinMode(A1, OUTPUT); //Output pin of the diode (analog pin 1)
  pinMode(LEDPin, OUTPUT); //LED pin is output
  digitalWrite(A1, LOW); 
  Last = readTemperature(); //first value for PID calculation
  
  double temp = readTemperature(); //fills temperature array for initial average calculation
  for(int i = 0; i < len; i++)
    prevTemps[i] = temp;
}

void loop() { 
  double currentTemp = readTemperature(); //stores the current temperature in a variable called currentTemp 
  double ave = getAve(); // gets current average
  
  if(badReading(currentTemp)) 
    currentTemp = getAve(); //using average if current reading is "outlier"
  else
    recordTemp(currentTemp); //records the temperature for calculating average later
  
  int drive = 0; //Current drive value is 0, so no PID is used. If using PID, comment this line out
    
  //*Uncomment below part to do PID stuff
  //int drive = getPID(); //calculates what drive value (out of 255) to use for PWM. Proportional to duty cycle (i.e. 51/255 = 0.2, meaning 20% duty cycle)
  //analogWrite(peltPin, drive);  //writes drive value to small Peltier
  //analogWrite(peltPin1, drive); //writes drive value to large Peltier

  OutputVoltage(outV, psuV, peltPin); // smaller & orange (max 14.4V and 6.4A). TEC1-12706
  OutputVoltage(outV, psuV, peltPin1);//bigger & gray (max 14.5V and 14.7A).  UT15

  checkSafe(ave);//goes to safety mechanism to turn off if getting too hot

  //turn on LED if system is around target Temp
  if(ave > tempThresh)
    digitalWrite(LEDPin, LOW);
  else
    digitalWrite(LEDPin, HIGH);

  Serial.print(currentTemp); //prints the target temp. This is what the python script cares about
    
  double raw = analogRead(A0); //reads the raw value from the diode
  Serial.print("    Raw: ");
  Serial.print(raw); //prints out the raw value 
  
  Serial.print("    T: ");
  Serial.print(currentTemp); //prints out the current temperature

  Serial.print("    Tf: ");
  Serial.print(getF(currentTemp)); //prints out the current temperature in fahrenheit
  
  Serial.print("   TAve: ");
  Serial.print(ave); //prints out the calculated real-time average
  
  Serial.print("   Dr:");
  Serial.println(drive); //prints out what the drive value is 
  
  delay(100); //At the end of the loop, delays for 100 milliseconds. Gives Arduino a break. 
  //end of the loop; goes back to the beginning of the loop
}




/*FUNCTIONS:
 * These don't do anything until you call them
 * 
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
  if(reachedOn == false && ave < onThresh) //increase the counter to reach the on state
    changeCount +=1;
    
  if(changeCount >= 30 && reachedOn == false){ //if 30 counts met, turns the mechanism on (on state)
    changeCount = 0;
    reachedOn = true;
  }

  if(reachedOn == true && ave >= badThresh) //increase the counter to reach the "problem state". Must be in on state
    changeCount +=1;

  if(reachedOn == true && ave < badThresh) //Makes it so the counts must be consecutive.
    changeCount = 0;
    
  if(changeCount >= 30 && reachedOn == true){ //if 30 counts met, the mechanism reports a problem and turns off the Peltiers
    changeCount = 0;
    outV = 0;
    for(int i = 0; i < 3; i++)  //Signaling to Python so it can email
      Serial.println("failure");//sent three times just in case
      
  }
}

int getPID(){ //function that calculates and returns PID value.  
  Actual = readTemperature();
  Error = Actual - targetTemp;

  if(abs(Error)<IntThresh && abs(Last-Actual) < 4){ //preventing spikes
    Integral = Integral + Error;
  }
  else{
    Integral = 0;
    //for(int j = 0; j < 10; j++)
      //Serial.println("stop");
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

boolean badReading(double temp){
  double ave = getAve();
  if(abs(temp-ave) >=3 && badReadings < 5){//To ignore spikes or misreadings, this will only allow readings 3 degrees from the average
    badReadings++; //If there are enough bad readings, they might actually be right. If high enough, will now trust these "bad" readings
    return true;
  }
  else{
    badReadings = 0;  //must be consecutive
    return false;
  }
}

void recordTemp(double temp){ //records temperature for calculating average
  for(int i = len-1; i > 0 ; i--){
    prevTemps[i] = prevTemps[i-1];
  }
  prevTemps[0] = temp;
}

double getAve(){ //calculates and returns average
  double sum = 0;
  for(int i = 0; i < len; i++)
    sum += prevTemps[i];
  return (double)(sum / len); 
}

double readTemperature(){ //calculates and returns temperature. 
  double in = analogRead(A0); //gets the raw "temperature value" from the diode
  c = (-0.5584*in) + 357.63;
  return c;
}

double getF(double C){ //converts C to F
  return (9*(C/5) + 32);
}

void OutputVoltage(double v, double SrcV, int pin) { //uses PWM to output voltage using calculated duty cycle. Ex: v = 2.4, SrcV = 12. Uses a 20% duty cycle
  analogWrite(pin, (v / SrcV) * 255);
}
