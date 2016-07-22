#Useful Resources- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import time
import io
import serial.tools.list_ports
import serial
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code
import matplotlib.pyplot as plt
import csv
import smtplib 

Temps = () #tuple to store temperatures for average temperature calculations
EmailSent = False #Only send the email alert once
LastTempKnown = 22 #Used for email alert in case tuple is reset. Default is 22, or room temp
Program_Start_Time = time.strftime("%Y%m%dT%H%M%S") #Time program began. For log file name
Program_Start_Time_Long = time.time() #used for plotting x variable
def SIGINT_handler(signal, frame): #Handling program exit
        print('Quitting program!')
        ser.close() #Ends serial connection
        sys.exit(0)

def getTemp(msg):
    for i in range(len(msg)): #the instantaneous temperature is the first "word" in the message
        if(msg[i:i+1] == " "): #The space indicates a new word, so the extraction of the first word is stopped
            return msg[0:i] 
    return -999 #If not found, -999 is sent
 
def recordTemp(temp): #Adds the temp to the tuple for later average calculations
    global Temps
    try: 
        Temps = Temps + (float(temp),) 
    except:
        pass
    
def resetTemps(): #Clears the tuple for new average calculations
    global Temps
    Temps = ()
    
def getTempAve(): #Average temperature over the out_Period
    global Temps
    sum = 0
    for i in Temps:
        sum += i
    return (sum / len(Temps))	#returns the average

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

#Outputs data into a text document. Sent to a directory named "Logs" and includes a timestamp. MUST HAVE "Logs" FOLDEER IN SAME DIRECTORY
def writeToTxt(now, msg):
    global Program_Start_Time
    with open("Logs\Log%s.txt"%(Program_Start_Time), "a") as f:        #Write to text document
        f.write("%s    %s\n" %(now, msg))    

#Outputs data into a csv file. Sent to a directory named "Logs" and includes a timestamp. MUST HAVE "Logs" FOLDEER IN SAME DIRECTORY
def writeToCsv(now, msg):
    global Program_Start_Time
    #fileDir = 'Logs\Log%s.csv'%(Program_Start_Time)
    with open('Logs\Log%s.csv'%(Program_Start_Time), 'ab') as csvfile: #Write to csv file
        writer = csv.writer(csvfile)
	writer.writerow([now, str(msg)])

#Sending emails if the arduino sends a failure message (i.e. "failure"). This happens when the circuit starts to heat up, which may indicate that the fan failed or something else failed.
def sendFailureEmail():
    fromaddr = 'peltier1w8cooler@gmail.com'
    #toaddrs = ['wei4wei@gmail.com', 'smcnama1@terpmail.umd.edu'] #testing emails
    toaddrs  = ['wei4wei@gmail.com', 'smcnama1@terpmail.umd.edu', 'mbreilly@hep.upenn.edu', 'mayers408@gmail.com', 'eress@sas.upenn.edu'] #all emails
    username = 'peltier1w8cooler@gmail.com'
    password = 'somethingbadhappened'
    
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
    except Exception:
        print "Failed to connect to email server\n"
    
    #Finding the best temperature to notify
    temp = "unknown"
    if(len(Temps) > 0):
        temp = str(getTempAve())
    elif(len(str(LastTempKnown)) > 0):
        temp = str(LastTempKnown)
        
    for addr in toaddrs:
        msg = "\r\n".join([
        "From: %s"%fromaddr,
        "To: %s"%addr,
        "Subject: Failure",
        "",
        "Something failed in the peltier setup. Possibly check it out if you are around. The last known temp is %sC. This may not be urgent; the Peltiers have already been turned off."%temp
        ])
        try:
            server.sendmail(fromaddr, addr, msg)
        except Exception:
            print "Email failed to send\n"
    try:
        server.quit()
    except Exception:
        print "Failed to disconnect to email server\n"
    
#Plotting the data in matplotlib
plt.ion()
plt.xlabel("Hours since %s"%Program_Start_Time)
plt.ylabel("Temperature (C)")
plt.title("Temperature vs. Time")
maxX = 0.001
maxY = 5
minY = -5
def updateMaxMins(x,y):#Updating max/mins for the boundaries of the graph
    global maxX,maxY,minY  
    if(x > maxX - 0.01): #+ and - give a better spaced/looking graph
        maxX = x + 0.01
    if(y > maxY - 3):
        maxY = y + 3
    if(y < minY + 3):
        minY = y - 3  

def plotData(x,y): #graphing the data in matplotlib
    global maxX,maxY,minY
    updateMaxMins(x,y)    
    plt.axis([0, maxX , minY, maxY]) #boundaries
    plt.scatter(x, y)
    plt.pause(out_period)

Start = time.time() #reference time point for the output period.
syncToBoard()	#Makes sure the script doesn't start in the middle of a line
while(1):     #Main loop
    msg = ""
    mycmd = ""

    while(mycmd != "\n"): #Adds characters to msg until new line. Basically a readline
        msg += mycmd
        mycmd=ser.read()
       
    
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
            if(msg != "No temperature data"):
                writeToCsv(now, msg) #Write the data to csv file
                plotData(float((time.time()-Program_Start_Time_Long)/3600), float(msg)) 
                #plots the temperature vs. hours since start
        


