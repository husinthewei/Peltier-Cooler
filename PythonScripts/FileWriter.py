import csv
class FileWriter:
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
