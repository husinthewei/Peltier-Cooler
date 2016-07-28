import csv
class FileWriter:
    #Outputs data into a text document. Sent to a directory named "Logs" and includes a timestamp. MUST HAVE "Logs" FOLDER IN SAME DIRECTORY AS PYTHON SCRIPT
    def writeToTxt(self, Program_Start_Time, now, msg):
        with open("Logs\Log%s.txt"%(Program_Start_Time), "a") as f:        #Write to text document
            f.write("%s    %s\n" %(now, msg))    

    #Outputs data into a csv file. Sent to a directory named "Logs" and includes a timestamp. MUST HAVE "Logs" FOLDER IN SAME DIRECTORY AS PYTHON SCRIPT
    def writeToCsv(self, Program_Start_Time, now, msg):
        with open('Logs\Log%s.csv'%(Program_Start_Time), 'ab') as csvfile: #Write to csv file
            writer = csv.writer(csvfile)
 	    writer.writerow([now, str(msg)])
