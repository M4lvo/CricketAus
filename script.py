# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 19:23:04 2020

@author: Ali Zohair
"""

import pandas as pd

#Function for returning 0 when there is no wicket or the wicket doesn't go into
#bowler's credit and 1 when there is a wicket taken by the bowler
def dismissal (row):
    if row['Batter Out']==0:
        return 0
    else:
        if row['How Out'] in ['RO','RH','R']:
            return 0
        else:
            return 1

#Importing the raw csv file
data = pd.read_csv('Deliveries-reduced.csv')

#Unwanted columns are dropped by using a list of wanted columns
wanted_Cols = ['Match Id','Match Date','Match Type','Season','Bowler Id',
               'Bowler','Bowler Hand','Pace / Spin','Bowler Style','Over','Bat Score','Wides',
               'Noballs','Byes','Legbyes','Penalty Runs','Batter Out','How Out','MatchInnings','Fair Ball In Over']
for col in data.columns:
    if col not in wanted_Cols:
        del(data[col])

#Computing total runs conceded in a single ball
data['Runs'] = data['Bat Score'] + data['Wides'] + data['Noballs'] + data[
        'Byes'] + data['Legbyes'] + data['Penalty Runs']
data.drop(['Bat Score','Wides','Noballs','Byes',
           'Legbyes','Penalty Runs'],axis=1,inplace=True)

#Using "dismissal" function on each row after nan values
#are replaced with a 0 to fill a new column named Wicket
data['Batter Out'].fillna(0,inplace=True)
data['Wicket'] = data.apply (lambda row: dismissal(row), axis=1)
data.drop(['Batter Out','How Out'],axis=1,inplace=True)

#Conversion of number categorical variables from int
#to string and renaming column for ease
data['Match Id'] = data['Match Id'].apply(str)
data['Bowler Id'] = data['Bowler Id'].apply(str)
data['Over'] = data['Over'].apply(str)
data['MatchInnings'] = data['MatchInnings'].apply(str)
data.rename(columns={'Fair Ball In Over': 'Balls'}, inplace=True)

#Creating groups on the decided levels with a single over being the lowest one
grouplevels = data.groupby(['Match Id','Match Date','Match Type','Season',
                            'Bowler Id','Bowler','Bowler Hand','Pace / Spin',
                            'Bowler Style','Over','MatchInnings'],as_index=False)
#Aggregating Runs, Wickets and Balls with summing
#up the first two and using max for the Balls
W_R_B = grouplevels.agg({"Runs":"sum","Wicket":"sum","Balls":"max"})
#Fixing rows where balls per over are greater than 6
W_R_B.loc[W_R_B['Balls']>6,'Balls'] = 6

#Exporting the resulting dataframe into a new csv
#after sorting them
W_R_B['Over'] = W_R_B['Over'].astype('int64')
W_R_B.sort_values(by=['Match Id','Match Date','Match Type',
            'Season','MatchInnings','Over'],inplace=True)
export_csv = W_R_B.to_csv (r'Overs.csv', index = None, header=True)