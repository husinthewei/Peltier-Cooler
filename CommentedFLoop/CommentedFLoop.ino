/*
 * Commented version of the feedback loop
 * 
 * If things are not commented, they are probably not useful to you. 
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
 * What will probably be useful for you:
 * 1. OutputVoltage(v, SrcV, pin); v = voltage you want to output, SrcV is what the voltage of the power supply is, and pin is the pin number/variable
 * 2. readTemperature(); Calculates the temperature from raw input. You will probably need to edit the equation in the function after you calibrate the diode again.
 * 3. getPID(); Calculates the PID pwn value (out of 255) to output to the arduino. You will probably have to modify the coefficients to make it work well. 
 * 
 * 
 * Note: If something is unclear, definitely email or facebook message me.
 */

 
int targetTemp = -2; //setting temporary target temp. Attempts to stay at this.
//PID stuff: Values for PID calculation
int Actual = 0; 
int Error = 0;
int Integral = 0;
int Last = 0;
int IntThresh = targetTemp + 5;
double kP = 8;   //P coefficient: modify if your are calibrating PID 
double kI = 0.3; //Integral coefficient
double kD = 0.3; //Derivative coefficient
int ScaleFactor = 1;
//
const int len = 10; //How many samples to use for the average. The time the sample is over is the number of samples divided by 10 (i.e. 10 samples / 10 = 1 second)
double prevTemps[len];
double averageTemp;
//
int peltPin = 3; //peltier cooler pin (smaller peltier on board)
int peltPin1 = 6; //second peliter cooler pin (big peltier connected to heatsink)
//
double psuV = 12; //Value used for calculation in OutputVoltage();
//
float c;
//
void setup() {
  pinMode(peltPin, OUTPUT); 
  pinMode(peltPin1, OUTPUT);
  Serial.begin(9600); 
  analogReference(INTERNAL); //Brings the reference voltage to 1.1v so that diode has more resolution.
  pinMode(A0, INPUT_PULLUP); //Declares as input and uses the 10k resistor as pullup. This is the input pin of the diode (analog pin 0)
  pinMode(A1, OUTPUT); //Output pin of the diode (analog pin 1)
  digitalWrite(A1, LOW); 
  Last = analogRead(A0);

  double temp = readTemperature();
  for(int i = 0; i < len; i++)
    prevTemps[i] = temp;
}

void loop() { 
  double currentTemp = readTemperature(); //stores the current temperature in a variable called currentTemp 
  recordTemp(currentTemp); //records the temperature for calculating average later
  
  int drive = 0; //Current drive value is 0, so no PID is used. If using PID, comment this line out
    
  //*Uncomment below part to do PID stuff
  //int drive = getPID(); //calculates what drive value (out of 255) to use for PWM. Proportional to duty cycle (i.e. 51/255 = 0.2, meaning 20% duty cycle)
  //analogWrite(peltPin, drive);  //writes drive value to small Peltier
  //analogWrite(peltPin1, drive); //writes drive value to large Peltier

  OutputVoltage(5, psuV, peltPin); // smaller & orange (max 8.6V, and 6A) Max 9.5
  OutputVoltage(5, psuV, peltPin1);//bigger & gray (max 14.5V, and 14.7A)

  double raw = analogRead(A0); //reads the raw value from the diode
  Serial.print(raw); //prints out the raw value
  
  Serial.print("    T: ");
  Serial.print(currentTemp); //prints out the current temperature

  Serial.print("   TAve: ");
  Serial.print(getAve()); //prints out the calculated real-time average
  
  Serial.print("   Dr:");
  Serial.println(drive); //prints out what the drive value is 
  
  delay(100); //At the end of the loop, delays for 100 milliseconds. Gives Arduino a break. 

  //end of the loop; goes back to the beginning of the loop
}




/*FUNCTIONS:
 * These don't do anything until you call them
 * getPid(); calculates PID value and returns it. Can be used like:  int drive = getPID(); 
 * recordTemp(temp); Takes the parameter (temp) and stores it for average calculation. Can be used like:  recordTemp(currentTemp);
 * getAve(); Calculates the average. Can be used like: double average = getAve()
 * readTemperature(); Calculates temperature form raw input and returns it. Can be used like:  double currentTemp = readTemperature();
 * OutputVoltage(v, SrcV, pin); Calculates duty cycle to use to reach v from the SrcV (source voltage) and outputs it to the pin. Can be used like: OutputVoltage(3, psuV, peltPin);
 */

int getPID(){ //function that calculates and returns PID value.  
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

  //this if statement is kind of like a piecewise function. If raw is less than 622, use one equation; otherwise, use the other
  if(in<=622)
    c = (-0.3234*in)+220.1; //first equation
  else
    c = (-0.6932*in)+450.08;//seconds equation

  //If you find a better equation for temperature that does not require a piecewise function, comment the piecewise and use something like...
  //c = (-21321 * in) + 1231;
    
  return c;
}
void OutputVoltage(double v, double SrcV, int pin) { //uses PWM to output voltage using calculated duty cycle. Ex: v = 2.4, SrcV = 12. Uses a 20% duty cycle
  analogWrite(pin, (v / SrcV) * 255);
}
