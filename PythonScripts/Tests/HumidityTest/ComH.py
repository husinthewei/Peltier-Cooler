#Useful Resources- http://forum.arduino.cc/index.php?topic=92457.0
#http://goo.gl/urER4U
import signal # For trapping ctrl-c or SIGINT
import sys # For exiting program with exit code
import SerialHandlerH 
import TempHandlerH
import FileWriterH
import EmailerH
import GrapherH
import time 

#Objects created to handle different tasks
Serial_Handler = SerialHandlerH.SerialHandlerH() 
Temp_Handler = TempHandlerH.TempHandlerH() 
File_Writer = FileWriterH.FileWriterH() 
Failure_Emailer = EmailerH.EmailerH() 
Plotter = GrapherH.GrapherH(Serial_Handler.getStart_Time()) 

#Handling program exit. Closes serial connection.
#Also saves graph to pdf
def SIGINT_handler(signal, frame): 
        print('Quitting program!')
        Serial_Handler.close() 
        path = 'Logs\Log%s.csv'%(Serial_Handler.getStart_Time())
        Plotter.produceGraph(path) 
        sys.exit(0)
        
signal.signal(signal.SIGINT, SIGINT_handler)

#Perform the actions that happen every Out_Period
#Outputs the average temperature (stored in msg) over the Out_Period 
def onPeriod(): 
    global Start
    Start = time.time() 
    msg = Temp_Handler.getTempAve() 
    hmdty = Temp_Handler.getHumidityAve()
    Temp_Handler.resetTemps() 
    print ("%s    %s    %s" %(now, msg, hmdty)) 
    if(msg != "No temperature data"): 
        #File_Writer.writeToTxt(Serial_Handler.getStart_Time(), now, msg) 
        File_Writer.writeToCsv(Serial_Handler.getStart_Time(), now, msg) 
        Plotter.plotData(float((time.time()-Serial_Handler.getStart_Time_Long())/3600), float(msg)) 
      
      
Start = time.time()             
Serial_Handler.syncToBoard()	
#Main loop
while(1):                      
    msg = Serial_Handler.readLine() 
    if("failure" in str(msg) and Failure_Emailer.getEmailSent() == False): 
        Failure_Emailer.sendFailureEmail(Temp_Handler.getBestTemp()) 
        
    if(len(msg)>0 and "failure" not in str(msg)):
        now= time.strftime("%Y-%m-%dT%H:%M:%S")
        Temp_Handler.extractHumidity(msg) 
        msg = Temp_Handler.extractTemp(msg)
    
        dt = time.time() - Start
        if(dt >= Serial_Handler.getOut_Period()): 
            onPeriod() 
    Plotter.processEvents() #Also handles GUI events. Must be called frequently.