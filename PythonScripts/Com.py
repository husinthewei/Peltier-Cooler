#Useful Resources- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code
import SerialHandler
import TempHandler
import time

Serial_Handler = SerialHandler.SerialHandler()
Temp_Handler = TempHandler.TempHandler()


def SIGINT_handler(signal, frame): #Handling program exit
        print('Quitting program!')
        Serial_Handler.close() #Ends serial connection
        sys.exit(0)
        
signal.signal(signal.SIGINT, SIGINT_handler)


Start = time.time() #reference time point for the output period.
Serial_Handler.syncToBoard()	#Makes sure the script doesn't start in the middle of a line
while(1):     #Main loop
    msg = Serial_Handler.readLine()
    #if("failure" in str(msg) and EmailSent == False): #If failure message received, send the email alert
    #    sendFailureEmail()
    #    print "Email Sent"
    #    EmailSent = True;
    if(len(msg)>0 and "failure" not in str(msg)):
        now= time.strftime("%Y-%m-%dT%H:%M:%S") #ISO 8601 time format
        msg = Temp_Handler.extractTemp(msg) #Extract the current temperature from the message. Also records temp for average calcultion
    
        dt = time.time() - Start #calculate the delta t since the last output
        if(dt >= Serial_Handler.getOut_Period()): #output something if delta t is higher than the period
            Start = time.time() #reset the  reference point
            msg = Temp_Handler.getTempAve()
            Temp_Handler.resetTemps()
            print ("%s    %s" %(now, msg)) #Write the data to console
            #print dt
    #       if(msg != "No temperature data"):
    #            writeToTxt(now, msg) #Write the data to text document
    #            writeToCsv(now, msg) #Write the data to csv file
    #            plotData(float((time.time()-Program_Start_Time_Long)/3600), float(msg))
    #            plotCount+=1