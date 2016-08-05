import smtplib 

class EmailerH:
    
    #Boolean EmailSent allows the email to be sent only once
    def __init__(self, email_sent = False):
        self.EmailSent = email_sent 
        self.fromaddr = 'peltier1w8cooler@gmail.com'
        self.password = 'somethingbadhappened'
        self.toaddrs = ['wei4wei@gmail.com', 'smcnama1@terpmail.umd.edu'] #testing emails
        #self.toaddrs = ['wei4wei@gmail.com', 'smcnama1@terpmail.umd.edu', 'mbreilly@hep.upenn.edu', 'mayers408@gmail.com', 'eress@sas.upenn.edu'] #all emails

    #Sending emails if the arduino sends a failure message (i.e. "failure"). 
    #This happens when the circuit starts to heat up, which may indicate that the fan failed or something else failed.
    def sendFailureEmail(self, temp):    
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(self.fromaddr,self.password)
        except Exception:
            print "Failed to connect to email server\n"
            
        for addr in self.toaddrs:
            msg = "\r\n".join([
            "From: %s"%self.fromaddr,
            "To: %s"%addr,
            "Subject: Failure",
            "",
            "Something failed in the peltier setup. Possibly check it out if you are around. The last known temp is %sC. This may not be urgent; the Peltiers have already been turned off."%temp
            ])
            try:
                server.sendmail(self.fromaddr, addr, msg)
                print "Email sent to: %s"%addr
                self.EmailSent = True
            except Exception:
                print "Email failed to send to: %s"%addr
        try:
            server.quit()
        except Exception:
            print "Failed to disconnect to email server"
                    
    def getEmailSent(self):
        return self.EmailSent
    def setEmailSent(self, sent):
        self.EmailSent = sent