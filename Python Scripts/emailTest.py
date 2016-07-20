import smtplib
fromaddr = 'peltier1w8cooler@gmail.com'
toaddrs  = 'wei4wei@gmail.com'
msg = "\r\n".join([
  "From: %s"%fromaddr,
  "To: %s"%toaddrs,
  "Subject: Test email",
  "",
  "Test"
  ])
username = 'peltier1w8cooler@gmail.com'
password = 'somethingbadhappened'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
