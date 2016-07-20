#Useful Forum- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import time
import io
import serial.tools.list_ports
import serial
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code
import csv
import smtplib 

global temps
temps = ()
global EmailSent
EmailSent = False
global Program_Start_Time
Program_Start_Time = time.strftime("%Y%m%dT%H%M%S")

def SIGINT_handler(signal, frame):
        print('Quitting program!')
        ser.close()
        sys.exit(0)
def getTemp(msg):
    for i in range(len(msg)): #the instantaneous temperature is the first "word"
        if(msg[i:i+1] == " "):
            return msg[0:i]
    return -1
 
def recordTemp(temp):
    global temps
    temps = temps + (float(temp),) 
    
def resetTemps():
    global temps
    temps = ()
    
def getTempAve(): #Average over the out_Period
    global temps
    sum = 0
    for i in temps:
        sum += i
    return (sum / len(temps))

signal.signal(signal.SIGINT, SIGINT_handler)

port_names=[]
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

out_period = 0
while(out_period <0.1): 
    out_period = input('Output data how often(seconds)? Minimum 0.1s    ')

ser=serial.Serial(port=port_names[int(user_port_selection)],baudrate=9600,timeout=1)
    
def syncToBoard():
    mycmd = ""
    while(mycmd != "\n"):
        mycmd=ser.read()    

start = time.time()
syncToBoard()

def writeToTxt(now, msg):
    global Program_Start_Time
    with open("Logs\Log%s.txt"%(Program_Start_Time), "a") as f:        #Write to text document
        f.write("%s    %s\n" %(now, msg))    

def writeToCsv(now, msg):
    global Program_Start_Time
    #fileDir = 'Logs\Log%s.csv'%(Program_Start_Time)
    with open('Logs\Log%s.csv'%(Program_Start_Time), 'ab') as csvfile: #Write to csv file
        writer = csv.writer(csvfile)
	writer.writerow([now, str(msg)])

def sendFailureEmail():
    fromaddr = 'peltier1w8cooler@gmail.com'
    #toaddrs = ['wei4wei@gmail.com', 'smcnama1@terpmail.umd.edu'] #testing emails
    toaddrs  = ['wei4wei@gmail.com', 'smcnama1@terpmail.umd.edu', 'mbreilly@hep.upenn.edu', 'mayers408@gmail.com'] #all emails
    username = 'peltier1w8cooler@gmail.com'
    password = 'somethingbadhappened'
    
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
    except Exception:
        print "Failed to connect to email server\n"
    
    temp = "unknown"
    
    if(len(temps) > 0):
        temp = str(getTempAve())
    
    for addr in toaddrs:
        msg = "\r\n".join([
        "From: %s"%fromaddr,
        "To: %s"%addr,
        "Subject: Failure",
        "",
        "Something failed in the peltier setup. Possibly check it out. The current temperature is above 0C. This may not be urgent; the Peltiers have just been turned off."
        ])
        try:
            server.sendmail(fromaddr, addr, msg)
        except Exception:
            print "Email failed to send\n"
    try:
        server.quit()
    except Exception:
        print "Failed to disconnect to email server\n"
    
		
while(1):
    msg = ""
    mycmd = ""
    while(mycmd != "\n"):
        msg += mycmd
        mycmd=ser.read()
    global start
    global Program_Start_Time
    global EmailSent        
    
    if("failure" in str(msg) and EmailSent == False):
        sendFailureEmail()
        print "Email Sent"
        EmailSent = True;
    if(len(msg)>0 and msg != "failure"):
        now= time.strftime("%Y-%m-%dT%H:%M:%S") #ISO 8601 time format
        msg = getTemp(msg)
        recordTemp(msg)
        dt = time.time() - start
        if(dt >= out_period):
            start = time.time()
            msg = getTempAve()
            resetTemps()
	    #writeToTxt(now, msg)
            writeToCsv(now, msg)
            print ("%s    %s" %(now, msg))
        


