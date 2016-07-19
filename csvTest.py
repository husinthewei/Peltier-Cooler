import csv

with open('Log.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["07182016144336", "21"])
    writer.writerow(["07182016144341", "23"])
    writer.writerow(["07182016144346", "26"])
