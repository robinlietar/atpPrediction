import csv
import datetime

# Step 0: We already added two columns diretly on Excel that compute
# randomize the winner and the loser, we now have two players ID1, ID2 and
# a third column Winner that can be either 1 or 2


# Step 1: We are gonna change the date and walculate the number of days associated
# in order to compute a difference


csvfileRead = open('games_atp.csv','rb')
csvfileWrite = open('games_atp_prepared.csv','wb')

reader = csv.reader(csvfileRead, delimiter=';', quotechar='|')
writer = csv.writer(csvfileWrite, lineterminator='\n')

all = []

t= 0
row0 = reader.next()
row0.append('DATE_PARSED_GAME')
row0.append('DATE_NUMBER_GAME')
all.append(row0)

#print(row0)


for row in reader:
    dateString = row[5][:8]
    dateNumber = min(int(dateString[:2]),30) + int(dateString[3:5])*30 + int(dateString[6:8])*365
    dateString = '20' + dateString[6:8] + '-' + dateString[3:5] + '-' + dateString[:2]
    #datetime.datetime.strftime(dateString, "%d/%m/%Y")
    row.append(dateString)
    row.append(str(dateNumber))
    all.append(row)

    t = t + 1
    if t < 10:
        print ', '.join(row)
writer.writerows(all)
