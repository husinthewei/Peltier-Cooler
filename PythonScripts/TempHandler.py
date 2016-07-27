class TempHandler:
    def __init__(self):
        self.Temps = () #tuple to store temperatures for average temperature calculations
        self.LastTempKnown = 22 #Used for email alert in case tuple is reset. Default is 22, or room temp
    
    #Managing the temperature data
    def getLastTempKnown(self):
        return self.LastTempKnown
    def getTemps(self):
        return self.Temps        
    def setTemps(self, temps):
        self.Temps = temps        
    def recordTemp(self, temp):
        try: 
            self.Temps = self.Temps + (float(temp),) 
        except:
            pass      
    def resetTemps(self): #Clears the tuple for new average calculations
        self.Temps = () 
   
    #Calculate the average from the data
    def getTempAve(self): #Average temperature over the out_Period
        if(len(self.Temps) > 0):
            sum = 0
            for i in self.Temps:
                sum += i
            ave = (sum / len(self.Temps))
            self.LastTempKnown = ave
            return ave	#returns the average
        else:
            return "No temperature data"
            
    def getBestTemp(self): #returns the best temperature to notify. Used for quick email
        temp = "unknown"
        if(len(self.Temps) > 0):
            temp = str(self.getTempAve())
        elif(len(str(self.LastTempKnown)) > 0):
            temp = str(self.LastTempKnown)
        return temp
            
    #Extracting temperature from an Arduino message
    def extractTemp(self, msg):
        for i in range(len(msg)): #the instantaneous temperature is the first "word" in the message
            if(msg[i:i+1] == " "): #The space indicates a new word, so the extraction of the first word is stopped
                self.recordTemp(msg[0:i])
                return msg[0:i] 

        
        