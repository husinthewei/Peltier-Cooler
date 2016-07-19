#Useful Forum- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import time
import io
import serial.tools.list_ports
import serial
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code

temps = ()

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

start = time.time()

while(1):
    msg = ""
    mycmd = ""
    global start
    while(mycmd != "\n"):
        msg += mycmd
        mycmd=ser.read()
    
    
    
    if(len(msg)>0):
        now= time.strftime("%Y-%m-%dT%H:%M:%S") #ISO 8601 time format
        msg = getTemp(msg)
        print msg
        recordTemp(msg)
        dt = time.time() - start
        if(dt >= out_period):
            start = time.time()
            msg = getTempAve()
            resetTemps()
            print dt
            with open("Log.txt", "a") as f:
	       f.write("%s    %s\n" %(now, msg))
            print ("%s    %s" %(now, msg))


