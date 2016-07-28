#Useful Resources- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code
import SerialHandler 
import TempHandler
import FileWriter
import Emailer
import Grapher
import time 

#Objects created to handle different tasks
Serial_Handler = SerialHandler.SerialHandler() #Handles all serial communication. Also analyzes messages.
Temp_Handler = TempHandler.TempHandler() #Stores and calculates using temperature data.
File_Writer = FileWriter.FileWriter() #Writes data to txt/csv files.
Failure_Emailer = Emailer.Emailer() #Emails failure messages    
Plotter = Grapher.Grapher(Serial_Handler.getStart_Time()) #Graphs the data

def SIGINT_handler(signal, frame): #Handling program exit
        print('Quitting program!')
        Serial_Handler.close() #Ends serial connection
        sys.exit(0)
        
signal.signal(signal.SIGINT, SIGINT_handler)


def onPeriod(): #Perform the actions that happen every Out_Period
    global Start
    Start = time.time() #reset the  reference point for dt
    msg = Temp_Handler.getTempAve() #Get the average over the last Out_Period seconds
    Temp_Handler.resetTemps() #reset temps tuple for new average calculation
    print ("%s    %s" %(now, msg)) #Write the data to console
    if(msg != "No temperature data"): 
        #File_Writer.writeToTxt(Serial_Handler.getStart_Time(), now, msg) #Write the data to text document
        File_Writer.writeToCsv(Serial_Handler.getStart_Time(), now, msg) #Write the data to csv file named Log(start time)
        Plotter.plotData(float((time.time()-Serial_Handler.getStart_Time_Long())/3600), float(msg)) #Plot the data
      
      
Start = time.time()             #reference time point for the output period.
Serial_Handler.syncToBoard()	#Makes sure the script doesn't start in the middle of a line
while(1):                      #Main loop
    msg = Serial_Handler.readLine() #Read a line of the Arduino output
    if("failure" in str(msg) and Failure_Emailer.getEmailSent() == False): #If failure message received, send an email alert
        Failure_Emailer.sendFailureEmail(Temp_Handler.getBestTemp()) #Parameter includes temperature data to send in email.
    if(len(msg)>0 and "failure" not in str(msg)):
        now= time.strftime("%Y-%m-%dT%H:%M:%S") #ISO 8601 time format
        msg = Temp_Handler.extractTemp(msg) #Extract the current temperature from the message. Also records temp for average calcultion.
    
        dt = time.time() - Start #calculate the delta t since the last output
        if(dt >= Serial_Handler.getOut_Period()): #output something if delta t is higher than the period
            onPeriod() #Perform the actions that happen every Out_Period