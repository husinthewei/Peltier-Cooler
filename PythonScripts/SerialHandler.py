import time
import serial.tools.list_ports
import serial
class SerialHandler:
    
    def __init__(self):
        self.Start_Time = time.strftime("%Y%m%dT%H%M%S") #Time program began. For log file name + documents
        self.Start_Time_Long = time.time() #used for plotting x variable
        self.createConnection() #Asks COM port and establishes connection with it
        self.promptOutputPeriod() #Asks how often to output data
        
    def createConnection(self):
        port_names=[]		#Having user select the correct COM port for the Arduino
        a=serial.tools.list_ports.comports()
        for w in a:
            port_names.append(w.device)
    
        port_names.sort()
        print('\nDetected the following serial ports:\nDon\'t choose /dev/ttyAMA0.')
        i=0
        for w in port_names:
            print('%d) %s' %(i,w))
            i=i+1
        total_ports=i # now i = total ports
        user_port_selection=input('\nSelect port: (0,1,2...)    ')
        if (int(user_port_selection)>=total_ports):
            print 'Port not in range'
            exit(1) # port selection out of range
        #Creating serial connection
        self.ser=serial.Serial(port=port_names[int(user_port_selection)],baudrate=9600,timeout=1)
        
    def promptOutputPeriod(self):
        #Having user select how frequently to output data
        self.Out_Period = 0
        while(self.Out_Period <0.1): 
            self.Out_Period = input('Output data how often(seconds)? Minimum 0.1s    ')
            
    #Makes sure this script does not start in the middle of one of the Arduino output lines
    def syncToBoard(self):
        mycmd = ""
        while(mycmd != "\n"):
            mycmd=self.ser.read() 
            
    def readLine(self): #Reads and returns a line of the arduino output
        msg = ""
        mycmd = ""
        try:
            while(mycmd != "\n"): #Adds characters to msg until new line. Basically a readline
                msg += mycmd
                mycmd=self.ser.read()
        except Exception:
            print "Serial Error"  
        return msg
    
    def close(self): #Close serial connection
        self.ser.close()
    
    #Getters and setters
    def getOut_Period(self):
        return self.Out_Period
    def getStart_Time(self):
        return self.Start_Time
    def getStart_Time_Long(self):
        return self.Start_Time_Long
        