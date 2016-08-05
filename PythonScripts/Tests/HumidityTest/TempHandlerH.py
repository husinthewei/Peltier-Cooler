class TempHandlerH:
    
    #Temp tuple stores temperatures for average calculations
    def __init__(self):
        self.Temps = ()
        self.Humidities = ()
        self.LastTempKnown = 22 
    
    def getLastTempKnown(self):
        return self.LastTempKnown
    def getTemps(self):
        return self.Temps        
    def setTemps(self, temps):
        self.Temps = temps      
        
    #Records data to tuple for average calculations.
    def recordTemp(self, temp): 
        try: 
            self.Temps = self.Temps + (float(temp),) 
        except:
            pass      
            
    #Records data to tuple for average calculations.            
    def recordHumidity(self, hmdty):
        try:
            self.Humidities = self.Humidities + (float(hmdty),)
        except:
            pass
                    
    #Clears the tuple for new average calculations        
    def resetTemps(self):
        self.Temps = () 
    def resetHumidities(self):
        self.Humidities = ()
   
    #Calculate the average from the data
    def getTempAve(self): 
        if(len(self.Temps) > 0):
            sum = 0
            for i in self.Temps:
                sum += i
            ave = (sum / len(self.Temps))
            self.LastTempKnown = ave
            return ave	
        else:
            return "No temperature data"
   
    #Calculate the average from the data
    def getHumidityAve(self): 
        if(len(self.Humidities) > 0):
            sum = 0
            for i in self.Humidities:
                sum += i
            ave = (sum / len(self.Humidities))
            return ave	
        else:
            return "No humidity data"
                         
    #returns the best temperature to notify. Used for quick email
    def getBestTemp(self):
        temp = "unknown"
        if(len(self.Temps) > 0):
            temp = str(self.getTempAve())
        elif(len(str(self.LastTempKnown)) > 0):
            temp = str(self.LastTempKnown)
        return temp
            
    #Extracting temperature from an Arduino message
    #The instantaneous temperature is the first "word" in the message
    def extractTemp(self, msg):
        for i in range(len(msg)): 
            if(msg[i:i+1] == " "): 
                self.recordTemp(msg[0:i])
                return msg[0:i] 

    #Extracting humidity from an Arduino message
    #The instantaneous temperature is the second "word" in the message
    def extractHumidity(self, msg):
        firstSpace = 0;
        for i in range(len(msg)): 
            if(msg[i:i+1] == " " and firstSpace != 0):
                self.recordHumidity(msg[firstSpace + 1: i])
                return msg[firstSpace + 1: i]
            if(msg[i:i+1] == " " and firstSpace == 0): 
                firstSpace = i

        