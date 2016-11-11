import csv

# Step 2 : Same preparation for ratings_atp

csvfileRead = open('ratings_atp.csv','rb')
csvfileWrite = open('ratings_atp_prepared.csv','wb')

reader = csv.reader(csvfileRead, delimiter=',', quotechar='|')
writer = csv.writer(csvfileWrite, lineterminator='\n')

all = []

t= 0
row0 = reader.next()
row0.append('DATE_PARSED_RATING')
row0.append('DATE_NUMBER_RATING')
all.append(row0)
print(row0)

for row in reader:
    dateString = row[0][:10]
    dateNumber = int(dateString[2:4])*365 + int(dateString[5:7])*30 + min(int(dateString[8:10]),30)
    row.append(dateString)
    row.append(str(dateNumber))
    all.append(row)

    t = t + 1
    if t < 10:
        print (row[0]) #', '.join
writer.writerows(all)
