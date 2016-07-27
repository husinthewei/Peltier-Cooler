class TempHandler:
    def __init__(self):
        self.Temps = () #tuple to store temperatures for average temperature calculations
        self.LastTempKnown = 22 #Used for email alert in case tuple is reset. Default is 22, or room temp
    
    #Managing the temperature data
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
        sum = 0
        for i in self.Temps:
            sum += i
        return (sum / len(self.Temps))	#returns the average
    
    #Extracting temperature from an Arduino message
    def extractTemp(msg):
        for i in range(len(msg)): #the instantaneous temperature is the first "word" in the message
            if(msg[i:i+1] == " "): #The space indicates a new word, so the extraction of the first word is stopped
                return msg[0:i] 
        return -999 #If not found, -999 is sent