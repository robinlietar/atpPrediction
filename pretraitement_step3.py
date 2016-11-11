import pandas as pd
import numpy as np

# Step 3 : Importing Games and Atp to join them using pandas

a = pd.read_csv("games_atp_prepared.csv")
b = pd.read_csv("ratings_atp_prepared.csv", error_bad_lines=False)
#print(b.shape)

# First merge, left join on the ID of the first player
merged = pd.merge(a, b,left_on=['ID1'], right_on=['ID_P_R'], how='left')

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
merged = merged.sort_values(by='DIFF_GAME_RATING_1').groupby(['ID1','ID2','DATE_PARSED_GAME'], as_index=False).first()


print (merged.head(n=5))
print(merged.shape)

#We lost 30000 rows, due to negative DATE_NUMBER_DIFFERENCE and some missing ratings
# We will then join our new merged with the initial games table

middle_merged = pd.merge(a,
            merged[['ID1','ID2','DATE_PARSED_GAME','POINT_R_1',
            'POS_R_1','DATE_PARSED_RATING_1', 'DIFF_GAME_RATING_1']],
            left_on=['ID1','ID2','DATE_PARSED_GAME'],
            right_on=['ID1','ID2','DATE_PARSED_GAME'], how='left')

print (middle_merged.head(n=5))
print(middle_merged.shape)








# Same job for ID2

# First merge, left join on the ID of the first player
merged = pd.merge(a, b,left_on=['ID2'], right_on=['ID_P_R'], how='left')

# Computing the difference between the date of the game and of the rating
merged['DATE_NUMBER_RATING'] = merged['DATE_NUMBER_GAME'] - merged['DATE_NUMBER_RATING']
d = list(merged.columns.values)

# Changing Column names
d[len(d) - 4] = 'POINT_R_2'
d[len(d) - 3] = 'POS_R_2'
d[len(d) - 2] = 'DATE_PARSED_RATING_2'
d[len(d) - 1] = 'DIFF_GAME_RATING_2'
merged.columns = d

#print(merged.shape)
#print (merged.head(n=5))

# Keeping only the ratings before the game
merged = merged[merged['DIFF_GAME_RATING_2'] >= 0.0]

#print (merged.head(n=5))
#print(merged.shape)

# Taking the minimum difference for every match
# between the date of the game and of the rating
merged = merged.sort_values(by='DIFF_GAME_RATING_2').groupby(['ID1','ID2','DATE_PARSED_GAME'], as_index=False).first()


print (merged.head(n=5))
print(merged.shape)

#We lost 30000 rows, due to negative DATE_NUMBER_DIFFERENCE and some missing ratings
# We will then join our new merged with the initial games table

final_merged = pd.merge(middle_merged,
            merged[['ID1','ID2','DATE_PARSED_GAME','POINT_R_2',
            'POS_R_2','DATE_PARSED_RATING_2', 'DIFF_GAME_RATING_2']],
            left_on=['ID1','ID2','DATE_PARSED_GAME'],
            right_on=['ID1','ID2','DATE_PARSED_GAME'], how='left')

print (final_merged.head(n=15))
print(final_merged.shape)


sLength = len(final_merged['ID1'])
#final_merged['DIFF_POINT'] = pd.Series(np.random.randn(sLength), index=final_merged.index)
#final_merged['DIFF_RATING'] = pd.Series(np.random.randn(sLength), index=final_merged.index)
final_merged['DIFF_POINT'] = final_merged['POINT_R_1'] - final_merged['POINT_R_2']
final_merged['DIFF_RATING'] = final_merged['POS_R_1'] - final_merged['POS_R_2']
final_merged['WINNER'] = final_merged['Winner']
final_merged['CORRECT'] = (((final_merged['Winner'] - 1)*2 - 1)*(final_merged['POS_R_1'] - final_merged['POS_R_2']) > 0)

rating_nan_number = final_merged[final_merged['DIFF_RATING'].isnull()]['ID1_G'].count()
correct_number = final_merged[final_merged['CORRECT']]['ID1_G'].count()
total_number = final_merged.shape[0]

percentage_rating = float(float(correct_number)/(total_number - rating_nan_number))
print (percentage_rating)

print (final_merged[final_merged['CORRECT']].head(n=25))
