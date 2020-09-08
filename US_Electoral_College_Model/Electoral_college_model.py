#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 19:05:29 2020

@author: Ned
"""
#%% Setup of year-based CSV files, and electoral vote values for each decade
import os
import wget
import pandas as pd
import numpy as np
import re
from voting import apportionment

pres_elect_state = pd.read_csv("1976-2016-president.csv")
pres_elect_state = pres_elect_state.drop(["state","state_fips",
                                          "state_cen","state_ic",
                                          "office","version","notes"],axis=1)
year_list = [1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016]
pres_elect_state = pres_elect_state.fillna(value='Blank')
pres_elect_state = pres_elect_state.reset_index(drop=True) 
for index, row in pres_elect_state.iterrows():
    if row.candidate == ('Blank Vote'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == ('Not Designated') and row.candidatevotes == 148353:
        pres_elect_state.at[index, 'candidate'] = 'Nader, Ralph'
        pres_elect_state.at[index, 'candidatevotes'] = 117857
        pres_elect_state.at[index, 'party'] = 'green'
    elif row.candidate == ('The Better Life,'):
        pres_elect_state.at[index, 'candidate'] = 'Nader, Ralph'
    elif row.candidate == ('Mitt, Romney'):
        pres_elect_state.at[index, 'candidate'] = 'Romney, Mitt'
    elif row.candidate == ('Blank'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == ('Blank Vote/Scattering'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == ('Blank Vote/Scattering'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == ('Blank Vote/Void Vote/Scattering'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == ('Other'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == ('Scattering'):
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
    elif row.candidate == 0:
        pres_elect_state.at[index,'candidate'] = 'writein'
    if row.party == 0:
        pres_elect_state.at[index,'party'] = 'independent'
        pres_elect_state = pres_elect_state.reset_index(drop=True) 
        
pres_elect_state = pres_elect_state.reset_index(drop=True)    
for index, row in pres_elect_state.iterrows():
    if (row.candidatevotes/row.totalvotes) < .018:
        pres_elect_state = pres_elect_state.drop(index = index, axis=0)
       
EC_votes_1970s = {
    "AL" : 9,"AK" : 3,"AZ" : 6,"AR" : 6,"CA" : 45,"CO" : 7,
    "CT" : 8,"DC" : 3,"DE" : 3,"FL" : 17,"GA" : 12,"HI" : 4,
    "ID" : 4,"IL" : 26,"IN" : 13,"IA" : 8,"KS" : 7,"KY" : 9,
    "LA" : 10,"ME" : 4,"MD" : 10,"MA" : 14,"MI" : 21,"MN" : 10,
    "MS" : 7,"MO" : 12,"MT" : 4,"NE" : 5,"NV" : 3,"NH" : 4,
    "NJ" : 17,"NM" : 4,"NY" : 41,"NC" : 13,"ND" : 3,"OH" : 25,
    "OK" : 8,"OR" : 6,"PA" : 27,"RI" : 4,"SC" : 8,"SD" : 4,
    "TN" : 10,"TX" : 26,"UT" : 4,"VT" : 3,"VA" : 12,"WA" : 9,
    "WV" : 6,"WI" : 11,"WY" : 3
    }

EC_votes_1980s = {
    "AL" : 9,"AK" : 3,"AZ" : 7,"AR" : 6,"CA" : 47,"CO" : 8,
    "CT" : 8,"DC" : 3,"DE" : 3,"FL" : 21,"GA" : 12,"HI" : 4,
    "ID" : 4,"IL" : 24,"IN" : 12,"IA" : 8,"KS" : 7,"KY" : 9,
    "LA" : 10,"ME" : 4,"MD" : 10,"MA" : 13,"MI" : 20,"MN" : 10,
    "MS" : 7,"MO" : 11,"MT" : 4,"NE" : 5,"NV" : 4,"NH" : 4,
    "NJ" : 16,"NM" : 5,"NY" : 36,"NC" : 13,"ND" : 3,"OH" : 23,
    "OK" : 8,"OR" : 7,"PA" : 25,"RI" : 4,"SC" : 8,"SD" : 3,
    "TN" : 11,"TX" : 29,"UT" : 5,"VT" : 3,"VA" : 12,"WA" : 10,
    "WV" : 6,"WI" : 11,"WY" : 3
    }

EC_votes_1990s = {
    "AL" : 9,"AK" : 3,"AZ" : 8,"AR" : 6,"CA" : 54,"CO" : 8,
    "CT" : 8,"DC" : 3,"DE" : 3,"FL" : 25,"GA" : 13,"HI" : 4,
    "ID" : 4,"IL" : 22,"IN" : 12,"IA" : 7,"KS" : 6,"KY" : 8,
    "LA" : 9,"ME" : 4,"MD" : 10,"MA" : 12,"MI" : 18,"MN" : 10,
    "MS" : 7,"MO" : 11,"MT" : 3,"NE" : 5,"NV" : 4,"NH" : 4,
    "NJ" : 15,"NM" : 5,"NY" : 33,"NC" : 14,"ND" : 3,"OH" : 21,
    "OK" : 8,"OR" : 7,"PA" : 23,"RI" : 4,"SC" : 8,"SD" : 3,
    "TN" : 11,"TX" : 32,"UT" : 5,"VT" : 3,"VA" : 13,"WA" : 11,
    "WV" : 5,"WI" : 11,"WY" : 3
    }

EC_votes_2000s = {
    "AL" : 9,"AK" : 3,"AZ" : 10,"AR" : 6,"CA" : 55,"CO" : 9,
    "CT" : 7,"DC" : 3,"DE" : 3,"FL" : 27,"GA" : 15,"HI" : 4,
    "ID" : 4,"IL" : 21,"IN" : 11,"IA" : 7,"KS" : 6,"KY" : 8,
    "LA" : 9,"ME" : 4,"MD" : 10,"MA" : 12,"MI" : 17,"MN" : 10,
    "MS" : 6,"MO" : 11,"MT" : 3,"NE" : 5,"NV" : 5,"NH" : 4,
    "NJ" : 15,"NM" : 5,"NY" : 31,"NC" : 15,"ND" : 3,"OH" : 20,
    "OK" : 7,"OR" : 7,"PA" : 21,"RI" : 4,"SC" : 8,"SD" : 3,
    "TN" : 11,"TX" : 34,"UT" : 5,"VT" : 3,"VA" : 13,"WA" : 11,
    "WV" : 5,"WI" : 10,"WY" : 3
    }

EC_votes_2010s = {
    "AL" : 9,"AK" : 3,"AZ" : 11,"AR" : 6,"CA" : 55,"CO" : 9,
    "CT" : 7,"DC" : 3,"DE" : 3,"FL" : 29,"GA" : 16,"HI" : 4,
    "ID" : 4,"IL" : 20,"IN" : 11,"IA" : 6,"KS" : 6,"KY" : 8,
    "LA" : 8,"ME" : 4,"MD" : 10,"MA" : 11,"MI" : 16,"MN" : 10,
    "MS" : 6,"MO" : 10,"MT" : 3,"NE" : 5,"NV" : 6,"NH" : 4,
    "NJ" : 14,"NM" : 5,"NY" : 29,"NC" : 15,"ND" : 3,"OH" : 18,
    "OK" : 7,"OR" : 7,"PA" : 20,"RI" : 4,"SC" : 9,"SD" : 3,
    "TN" : 11,"TX" : 38,"UT" : 6,"VT" : 3,"VA" : 13,"WA" : 12,
    "WV" : 5,"WI" : 10,"WY" : 3
    }

path = os.getcwd() + "/election_years"
try:
    os.mkdir(path, exist_ok = True)
except:
    pass
else:
    pass

for year in year_list:
    current_year = year
    current_df = pres_elect_state['year']==current_year
    current_df = pres_elect_state[current_df]        
    current_df.to_csv("election_years/pres_{0}.csv".format(year))
    
#%% Iterating through values and transforming data into a tidy format
state_list = list(pres_elect_state.iloc[:, 1].unique())    
df_list = ["pres_1976.csv","pres_1980.csv","pres_1984.csv","pres_1988.csv",
           "pres_1992.csv","pres_1996.csv","pres_2000.csv","pres_2004.csv",
           "pres_2008.csv","pres_2012.csv","pres_2016.csv"]

for df in df_list:
    current_year = pd.read_csv("election_years/" + df)
    candidate_list = list(current_year.iloc[:, 3].unique())
    for state in state_list:
        current_state_bool = current_year['state_po']==state
        current_state = current_year[current_state_bool]
        if state == 'NY':
            current_votes = current_state.filter(items=['candidate',
                                                        'candidatevotes',
                                                        'party'])
            for index, row in current_votes.iterrows():
                if row.party == 'democrat':
                    demvotes = row.candidatevotes
                    dem = row.candidate
                elif row.party == 'republican':
                    gopvotes = row.candidatevotes
                    gop = row.candidate
                elif row.candidate == dem:
                    demvotes += row.candidatevotes
                elif row.candidate == gop:
                    gopvotes += row.candidatevotes
            for index, row in current_votes.iterrows():
                if row.candidate == dem and row.party != 'democrat':
                    current_votes = current_votes.drop(index = index, axis=0)
                elif row.candidate == gop and row.party != 'republican':
                    current_votes = current_votes.drop(index = index, axis=0)
            current_votes.loc[current_votes.party == 'democrat', 'candidatevotes'] = demvotes
            current_votes.loc[current_votes.party == 'republican', 'candidatevotes'] = gopvotes
            current_votes = current_votes.filter(items=['candidate','candidatevotes'])
        elif state == 'SC' and df == 'pres_1996.csv':
            current_votes = current_state.filter(items=['candidate','candidatevotes','party'])
            reformvotes = 0
            reform = 'Perot, Ross'
            for index, row in current_votes.iterrows():
                if row.candidate == reform:
                    reformvotes += row.candidatevotes
                elif row.candidate != 'Perot, Ross':
                    continue
            for index, row in current_votes.iterrows():
                if row.candidate == reform and row.party != 'reform party':
                    current_votes = current_votes.drop(index = index, axis=0) 
            current_votes.loc[current_votes.candidate == reform, 'candidatevotes'] = reformvotes
            current_votes = current_votes.filter(items=['candidate','candidatevotes'])
        else: 
            current_votes = current_state.filter(items=['candidate','candidatevotes'])
        new_state = current_votes.transpose()   
        new_state = new_state.rename(columns = new_state.iloc[0,])
        new_state = new_state.rename(index={'candidatevotes' : 0})
        new_state = new_state.drop('candidate')
        new_state['totalvotes'] = current_state.iloc[0,7]
        new_state['state'] = current_state.iloc[0,2]
        new_state['year'] = current_state.iloc[0,1]
        cols = new_state.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        new_state = new_state[cols]
        if state == 'AL':
            year_df = new_state
        else: 
            year_df = pd.concat([year_df,new_state], ignore_index = True, axis = 0)
        df1 = year_df.pop('totalvotes')
        year_df['totalvotes']=df1
    if df == 'pres_1976.csv' or df == 'pres_1980.csv':
        year_df['ECvotes']= year_df['state'].map(EC_votes_1970s)
    if df == 'pres_1984.csv' or df =='pres_1988.csv':
        year_df['ECvotes']= year_df['state'].map(EC_votes_1980s)
    if df == 'pres_1992.csv' or df == 'pres_1996.csv' or 'pres_2000.csv':
        year_df['ECvotes']= year_df['state'].map(EC_votes_1990s)    
    if df == 'pres_2004.csv' or df == 'pres_2008.csv':
        year_df['ECvotes']= year_df['state'].map(EC_votes_2000s)
    if df == 'pres_2012.csv' or df == 'pres_2016.csv':
        year_df['ECvotes']= year_df['state'].map(EC_votes_2010s)
    globals() [re.sub('.csv', '', df) + "_votes"] = year_df
    current_year = list(year_df.values.tolist())[1][1]
    year_df.to_csv("election_years/pres_{0}.csv".format(current_year))
    
#%% d'Hondt method apportionment of electoral votes, and creation of summary stats

df_list = (pres_1976_votes, pres_1980_votes, pres_1984_votes, pres_1988_votes, 
           pres_1992_votes, pres_1996_votes, pres_2000_votes, pres_2004_votes, 
           pres_2008_votes, pres_2012_votes, pres_2016_votes)
count = 0
EC_colnames = []
for year in year_list:
    EC_colnames.append('Candidate')
    EC_colnames.append(year)
# actual_results = pd.DataFrame('Candidate' : ['Carter, Jimmy','Ford, Gerald', )    
    
# EC_votes_dhondt = pd.DataFrame[]
for df in df_list:
    current_year = df.values.tolist()[1][1]
    sum_stats = df.sum()
    sum_stats = sum_stats.to_frame()
    sum_stats = sum_stats.drop(['state','year'])
    sum_stats = sum_stats.reset_index()
    sum_stats = sum_stats.rename(columns={"index" : 'Candidate', 0: 'Votes'})
    print(sum_stats)
    for index, row in sum_stats.iterrows():
        if row.Candidate == 'totalvotes':
            total = row.Votes
    for index, row in sum_stats.iterrows(): 
        if row.Candidate != 'ECvotes' and row.Candidate != 'totalvotes':
            sum_stats.at[index, 'Votes'] = (row.Votes / total * 100)
        else:
            sum_stats = sum_stats.drop(index = index)
    sum_stats = sum_stats.rename(columns={'Votes' : 'Popular_Vote'})
    # print(sum_stats)
        # if row.Candidate != 'ECvotes':
            # sum_stats.at[index, current_year] = 'Nader, Ralph'

    df = df.fillna(value=0)
    result_colnames = list(df.columns.values.tolist())
    result_colnames.remove('totalvotes')
    dhondt_results = pd.DataFrame([], columns = result_colnames)
    for index, row in df.iterrows():
        votes = row[2:(len(row)-2)]
        ec_votes = (row[(len(row)-1)])
        allocation = apportionment.dhondt(votes, ec_votes)
        allocation.append(ec_votes)
        allocation.insert(0,row.values[0])
        allocation.insert(0,row.values[1])
        df_length = len(dhondt_results)
        dhondt_results.loc[df_length] = allocation
    dhondt_sums = dhondt_results.drop(['year','state'], axis = 1)
    
    sums = dhondt_sums.sum(axis = 0, skipna = True)
    sums = sums.to_frame()
    sums = sums.reset_index()
    for index, row in sums.iterrows():
        if row.iloc[0] == ('ECvotes'):
            sums = sums.drop(index = index, axis=0)
    
    sums = sums.rename(columns={"index" : 'Candidate', 0: 'dHondt_EC'})
    sums = sums.merge(sum_stats, on = 'Candidate', how='outer')
    # sums.insert(2, "EC_Percentage", EC_percentage , True)
    NaN = np.nan
    sums.insert(2, 'EC_Percentage', NaN, allow_duplicates = False)
    sums.insert(4, 'Discrepancy', NaN, allow_duplicates = False)
    # sums['EC_Percentage'] = NaN
    for index, row in sums.iterrows():
        sums.at[index,'EC_Percentage'] = round((row.dHondt_EC / 538 * 100),2)
    for index, row in sums.iterrows():
        sums.at[index,'Discrepancy'] = round((row.Popular_Vote - row.EC_Percentage),2)
    # sums.append(pd.Series(), ignore_index=True)
    # sums.insert(1, 'Actual_EC', NaN, allow_duplicates = False)
    # if current_year == 1976:
        # sums.insert(1, 'Actual_EC', [297,240,0,0,0], allow_duplicates = False)
    row_df = pd.DataFrame([list(sums.columns.values.tolist())])
    row_df.columns = list(sums.columns.values.tolist())
    row_df.at[0, 'Candidate'] = np.NaN
    sums = pd.concat([row_df, sums], ignore_index=True)

    
    
    if count == 0:
        EC_votes_dhondt = sums
        count += 1
    elif count > 0:
        EC_votes_dhondt = EC_votes_dhondt.append(sums, ignore_index=True)
    
EC_votes_dhondt.insert(1, 'Actual_EC', ['1976_EC',297,241,0,0,0,
                                        '1980_EC',489,49,0,0,
                                        '1984_EC',525,13,0,
                                        '1988_EC',426,112,0,
                                        '1992_EC',168,370,0,0,
                                        '1996_EC',159,379,0,0,
                                        '2000_EC',271,267,0,0,
                                        '2004_EC',286,252,
                                        '2008_EC',173,365,0,
                                        '2012_EC',206,332,0,
                                        '2016_EC',306,232,0,0,0,0,0,
                                        ], allow_duplicates = False)
        
df1 =pd.DataFrame(['1976_Vote',50.08,48.02,0.21,0.91,0.19,
       '1980_Vote',50.75,41.01,1.06,6.61,
       '1984_Vote',58.77,40.56,0.25,
       '1988_Vote',53.37,45.65,0.47,
       '1992_Vote',37.45,43.01,18.91,0.10,
       '1996_Vote',40.71,49.24,8.40,0.71,
       '2000_Vote',47.87,48.38,2.74,0.43,
       '2004_Vote',50.73,48.27,
       '2008_Vote',45.65,52.93,0.03,
       '2012_Vote',47.20,51.06,0.99,
       '2016_Vote',46.09,48.18,3.28,1.07,0.54,0.02, 0.013,
       ])
    
EC_votes_dhondt['Popular_Vote'] = df1[0].values

for index, row in EC_votes_dhondt.iterrows():
        if row.EC_Percentage != 'EC_Percentage':
            EC_votes_dhondt.at[index,'Discrepancy'] = -(round((row.Popular_Vote - row.EC_Percentage),2))

EC_votes_
.to_csv("EC_results_dhondt.csv")   


    
    
