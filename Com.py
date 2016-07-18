#Useful Forum- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import time
import io
import serial.tools.list_ports
import serial
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code

def SIGINT_handler(signal, frame):
        print('Quitting program!')
        ser.close()
        sys.exit(0)

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

user_port_selection=input('\nSelect port: (0,1,2...)')
if (int(user_port_selection)>=total_ports):
    exit(1) # port selection out of range

ser=serial.Serial(port=port_names[int(user_port_selection)],baudrate=9600,timeout=0.1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
# ser=serial.Serial("COM1",baudrate=9600,timeout=10)
while(1):
    #mycmd=ser.read()
    mycmd = sio.readline();
    if (len(mycmd)>0):
        now= time.strftime("%d/%m/%Y  %H:%M:%S")
        with open("Log.txt", "w") as text_file:
            text_file.write("Purchase Amount: %s" % now)
        print (now)
        print(mycmd);
        #epoch=int(time.time())
        #ser.write(str(epoch).encode())
        ser.write(b'\n')

