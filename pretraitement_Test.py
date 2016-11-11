#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 15:34:20 2016

@author: robinlietar
"""

import csv
import datetime
import pandas as pd
import numpy as np

# Step 0: We already added two columns diretly on Excel that compute
# randomize the winner and the loser, we now have two players ID1_G, ID2_G and
# a third column Winner that can be either 1 or 2


# Step 1: We are gonna change the date and walculate the number of days associated
# in order to compute a difference


csvfileRead = open('games_atp_public.csv','rb')
csvfileWrite = open('games_atp_public_prepared.csv','wb')

reader = csv.reader(csvfileRead, delimiter=',', quotechar='|')
writer = csv.writer(csvfileWrite, lineterminator='\n')

all = []

t= 0
row0 = reader.next()
row0.append('DATE_PARSED_GAME')
row0.append('DATE_NUMBER_GAME')
all.append(row0)

#print(row0)


for row in reader:
    dateString = row[4][:10]
    dateNumber = int(dateString[2:4])*365 + int(dateString[5:7])*30 + min(int(dateString[8:10]),30)
    dateString = '20' + dateString[6:8] + '-' + dateString[3:5] + '-' + dateString[:2]
    #datetime.datetime.strftime(dateString, "%d/%m/%Y")
    row.append(dateString)
    row.append(str(dateNumber))
    all.append(row)

    t = t + 1
    if t < 10:
        print ', '.join(row)
writer.writerows(all)

# Step 3 : Importing Games and Atp to join them using pandas

a = pd.read_csv("games_atp_public_prepared.csv")
b = pd.read_csv("ratings_atp_prepared.csv", error_bad_lines=False)
#print(b.shape)

# First merge, left join on the ID of the first player
merged = pd.merge(a, b,left_on=['ID1_G'], right_on=['ID_P_R'], how='left')

# Computing the difference between the date of the game and of the rating
merged['DATE_NUMBER_RATING'] = merged['DATE_NUMBER_GAME'] - merged['DATE_NUMBER_RATING']
d = list(merged.columns.values)

# Changing Column names
d[len(d) - 4] = 'POINT_R_1'
d[len(d) - 3] = 'POS_R_1'
d[len(d) - 2] = 'DATE_PARSED_RATING_1'
d[len(d) - 1] = 'DIFF_GAME_RATING_1'
merged.columns = d

#print(merged.shape)
#print (merged.head(n=5))

# Keeping only the ratings before the game
merged = merged[merged['DIFF_GAME_RATING_1'] >= 0.0]

#print (merged.head(n=5))
#print(merged.shape)

# Taking the minimum difference for every match
# between the date of the game and of the rating
merged = merged.sort_values(by='DIFF_GAME_RATING_1').groupby(['ID1_G','ID2_G','DATE_PARSED_GAME'], as_index=False).first()


print (merged.head(n=5))
print(merged.shape)

#We lost 30000 rows, due to negative DATE_NUMBER_DIFFERENCE and some missing ratings
# We will then join our new merged with the initial games table

middle_merged = pd.merge(a,
            merged[['ID1_G','ID2_G','DATE_PARSED_GAME','POINT_R_1',
            'POS_R_1','DATE_PARSED_RATING_1', 'DIFF_GAME_RATING_1']],
            left_on=['ID1_G','ID2_G','DATE_PARSED_GAME'],
            right_on=['ID1_G','ID2_G','DATE_PARSED_GAME'], how='left')

merged = pd.merge(a, b,left_on=['ID2_G'], right_on=['ID_P_R'], how='left')
merged['DATE_NUMBER_RATING'] = merged['DATE_NUMBER_GAME'] - merged['DATE_NUMBER_RATING']
d = list(merged.columns.values)

d[len(d) - 4] = 'POINT_R_2'
d[len(d) - 3] = 'POS_R_2'
d[len(d) - 2] = 'DATE_PARSED_RATING_2'
d[len(d) - 1] = 'DIFF_GAME_RATING_2'
merged.columns = d

merged = merged[merged['DIFF_GAME_RATING_2'] >= 0.0]
merged = merged.sort_values(by='DIFF_GAME_RATING_2').groupby(['ID1_G','ID2_G','DATE_PARSED_GAME'], as_index=False).first()


print (merged.head(n=5))
print(merged.shape)

#We lost 30000 rows, due to negative DATE_NUMBER_DIFFERENCE and some missing ratings
# We will then join our new merged with the initial games table

final_merged = pd.merge(middle_merged,
            merged[['ID1_G','ID2_G','DATE_PARSED_GAME','POINT_R_2',
            'POS_R_2','DATE_PARSED_RATING_2', 'DIFF_GAME_RATING_2']],
            left_on=['ID1_G','ID2_G','DATE_PARSED_GAME'],
            right_on=['ID1_G','ID2_G','DATE_PARSED_GAME'], how='left')

print (final_merged.head(n=15))
print(final_merged.shape)

final_merged['DIFF_POINT'] = final_merged['POINT_R_1'] - final_merged['POINT_R_2']
final_merged['DIFF_RATING'] = final_merged['POS_R_1'] - final_merged['POS_R_2']
final_merged['PREDICTION'] = (np.sign(final_merged['POS_R_1'] - final_merged['POS_R_2'])+1)/2 + 1
rating_nan_number = final_merged[final_merged['PREDICTION'].isnull()]['ID1_G'].count()
print(rating_nan_number)

# we get the rating for 3368 out of 7608 games (a bit less than a half)
# we use the rule for the 3368 and then predict one for the others
# with this rule we get 57%

final_merged['PREDICTION'].fillna(1, inplace=True)
final_merged['PREDICTION'] = final_merged['PREDICTION'].astype(int)

final_merged[['ID1_G','ID2_G','ID_T_G','ID_R_G','PREDICTION']].to_csv('games_atp_public_final.csv', sep=',', index=False)

print (final_merged.head(n=15))
print(final_merged.shape)

#percentage_rating = float(float(correct_number)/(total_number - rating_nan_number))
#print (percentage_rating)

#print (final_merged[final_merged['CORRECT']].head(n=25))
