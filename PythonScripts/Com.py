#Useful Resources- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import time
import serial.tools.list_ports
import serial
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code

Program_Start_Time = time.strftime("%Y%m%dT%H%M%S") #Time program began. For log file name
Program_Start_Time_Long = time.time() #used for plotting x variable

def SIGINT_handler(signal, frame): #Handling program exit
        print('Quitting program!')
        ser.close() #Ends serial connection
        sys.exit(0)

signal.signal(signal.SIGINT, SIGINT_handler)

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
total_ports=i # now i= total ports

user_port_selection=input('\nSelect port: (0,1,2...)    ')
if (int(user_port_selection)>=total_ports):
    exit(1) # port selection out of range

#Having user select how frequently to output data
out_period = 0
while(out_period <0.1): 
    out_period = input('Output data how often(seconds)? Minimum 0.1s    ')

#Creating serial connection
ser=serial.Serial(port=port_names[int(user_port_selection)],baudrate=9600,timeout=1)
    
#Makes sure this script does not start in the middle of one of the Arduino output lines
def syncToBoard():
    mycmd = ""
    while(mycmd != "\n"):
        mycmd=ser.read()    


   
Start = time.time() #reference time point for the output period.
syncToBoard()	#Makes sure the script doesn't start in the middle of a line
plotCount =  0
while(1):     #Main loop
    msg = ""
    mycmd = ""

    try:
        while(mycmd != "\n"): #Adds characters to msg until new line. Basically a readline
            msg += mycmd
            mycmd=ser.read()
    except Exception:
         print "Serial Error"   
    
    if("failure" in str(msg) and EmailSent == False): #If failure message received, send the email alert
        sendFailureEmail()
        print "Email Sent"
        EmailSent = True;
    if(len(msg)>0 and "failure" not in str(msg)):
        now= time.strftime("%Y-%m-%dT%H:%M:%S") #ISO 8601 time format
        msg = getTemp(msg) #Extract the current temperature from the message
        if(msg != -999): #-999 means no temperature extracted
            recordTemp(msg) #Add the temperature to the tuple used to calculate averages
        
        dt = time.time() - Start #calculate the delta t since the last output
        if(dt >= out_period): #output something if delta t is higher than the period
            Start = time.time() #reset the  reference point
            if(len(Temps) > 0):
                msg = getTempAve() #the output message is the average from the tuple
                LastTempKnown = msg
            else:
                msg = "No temperature data"
            resetTemps() #reset the tuple
	    #writeToTxt(now, msg) #Write the data sto text document
            print ("%s    %s" %(now, msg)) #Write the data to console
            #print dt
            if(msg != "No temperature data"):
                writeToCsv(now, msg) #Write the data to csv file
                plotData(float((time.time()-Program_Start_Time_Long)/3600), float(msg))
                plotCount+=1
                #print plotCount
                #plots the temperature vs. hours for last 1000 samples