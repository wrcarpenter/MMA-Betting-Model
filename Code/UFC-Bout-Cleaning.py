"""

MMA Bout Cleaning 

Creator: Will Carpenter 

Description: Used for cleaning UFC data scraped online. This will work off the 
raw data to create a usable panel for model implementation. 

"""
#%%

# Importing
import requests
import csv 
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
# from google.colab import files
import datetime
from datetime import date
from pytz import timezone
eastern = timezone('US/Eastern')
import threading 
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
cores = multiprocessing.cpu_count()

#%%
# Upload most recent working version of bout data 
source = 'https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/ufcBouts_v5.csv'  
df      = pd.read_csv(source, header=0) 
df_orig = df # preserve a copy in case
del source

#%%
# Explore the dataset 
print(df.columns)
# Columns in dataset 
print(df.shape[1]) # raw dataset should have 28 columns? 
# Unique fighters
print("Number of Unique Fighters: ", len(pd.unique(df['name'])))  # unique fighters
# Number of fights (nows in dataset)
print("Total Fights Recorded: ", len(df))
# Number of unique fights in the dataset 
print("Number of Unique Fights: ", len(pd.unique(df['fight_link'])))

#%%

# Eliminate any missing DOB (can fill this in later)
df = df[df['dob'] != "--"]  # drops missing birthdays from the data 
print(len(df) - len(df_orig))  # drops 865 obs currently
# Sort dob
df['dob'] = df['dob'].replace(',', '', regex=True)  # replace commas
df['dob'] = df['dob'].replace('--', '', regex=True)  # replace commas
df['dob'] = pd.to_datetime(df['dob'], format="%m/%d/%Y")
# Sort event date
df['event_date'] = df['event_date'].replace(',', '', regex=True)  # replace commas 
df['event_date'] = pd.to_datetime(df['event_date'], format="%m/%d/%Y")
# Sorts in new data 
df = df.sort_values(by=['fighter_profile', 'event_date'], ascending=True)
# Show results
# df.loc[df['name'] == 'Jon Jones', ['event_date', 'event', 'total_fights']]
 
#%%
# Current age of fighter at date time (years)
df['current_age'] = (df['event_date'] - df['dob']) / np.timedelta64(1, 'Y')

# Number of previous recorded fights in data 
df['ones'] = 1
df['prev_num_fights'] = df.groupby(['fighter_profile'])['ones'].cumsum() - 1
# df.drop(columns=['total_fights'])

# Weeks since previous fight
# Weeks since will fill "N/A" if its the first fight in the dataset for a fighter
df['wks_since_last_fight'] = df.groupby(['fighter_profile'])['event_date'].diff()  # total time between date values
df['wks_since_last_fight'] = df['wks_since_last_fight'] / np.timedelta64(1, 'W')   # this includes some NaN

# Years since first recorded fight 
df['min_date']    = df.groupby(['fighter_profile'])['event_date'].min()
df['roster_time'] = (df['event_date'] - df['min_date']) / np.timedelta64(1, 'Y')
 
 
#%% 
 
# FIGHT RESULTS 

# Result of last fight 
# Need to breakdown the results by some kind of number pattern 
# Main fight results (binary variable)
df['win']        = df['fighter_result'].apply(lambda x: 1 if x == 'W' else 0)
df['loss']       = df['fighter_result'].apply(lambda x: 1 if x == 'L' else 0)
df['no_contest'] = df['fighter_result'].apply(lambda x: 1 if x == 'NC' else 0)
df['draw']       = df['fighter_result'].apply(lambda x: 1 if x == 'D' else 0)

# Granular result metrics (if betting on KO win or something else)
# there are some other fields included in these results
df['ko']  = df['method'].apply(lambda x: 1 if x == 'KO/TKO' or x == "TKO - Doctor's Stoppage" or x == "Could Not Continue" else 0)
df['sub'] = df['method'].apply(lambda x: 1 if x == 'Submission' else 0)
df['dec'] = df['method'].apply(lambda x: 1 if x == 'Decision - Unanimous' or x == "Decision - Split" or x == "Decision" else 0)

# Defining win categories for potential prediction 
df['ko_win']  = np.where(((df['ko'] == 1) & (df['win'] == 1 )), 1, 0)
df['sub_win'] = np.where(((df['sub'] == 1) & (df['win'] == 1 )), 1, 0) 
df['dec_win'] = np.where(((df['dec'] == 1) & (df['win'] == 1 )), 1, 0) 

# height,weight
# result of last fight (define categorical variables, ko_loss, ko_win, etc. )
# result of second to last fight

# Shifting for previous fight results 
# Issue here is that you are shifting up another fighters results to be the first observation!!!
df.groupby('object')['value'].shift()

# Should mark first fight, no previous data 
df['prev_fight_result'] = 0 

# Neither a 
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['win'].shift(1) == 0)&\
                                    (df.groupby('fighter_profile')['loss'].shift(1) == 0)),1,df['prev_fight_result'])
# Loss and KO result
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['loss'].shift(1) == 1)&\
                                    (df.groupby('fighter_profile')['ko'].shift(1) == 1)),2,df['prev_fight_result'])
    
# Loss and sub result
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['loss'].shift(1) == 1)&\
                                    (df.groupby('fighter_profile')['sub'].shift(1) == 1 )),3,df['prev_fight_result'])    
    
# Loss and dec result
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['loss'].shift(1) == 1)&\
                                    (df.groupby('fighter_profile')['dec'].shift(1) == 1 )),4,df['prev_fight_result'])     
         
df['prev_fight_result'] = np.where((df.groupby('fighter_profile')['dec_win'].shift(1) == 1),5,df['prev_fight_result'])
df['prev_fight_result'] = np.where((df.groupby('fighter_profile')['sub_win'].shift(1) == 1),6,df['prev_fight_result'])
df['prev_fight_result'] = np.where((df.groupby('fighter_profile')['ko_win'].shift(1) == 1),7,df['prev_fight_result'])
                                       
# Encoding 
# ko_win   = 7
# sub_win  = 6 
# dec_win  = 5
# dec_loss = 4
# sub_loss = 3 
# ko_loss = 2
# other   = 1
# first   = 0

# "Browsing tools 
browse_columns = ['name', 'fighter_result', 'event_date', 'method', 'win', 'loss', 'ko', 'sub', 'dec','ko_win', 'prev_fight_result','sub_win', 'dec_win']
# Browser for de-bugging 
df_browse = df[browse_columns]
df_browse_sample = df.loc[df['name'] == 'Jon Jones', browse_columns]

# Very useful commands
df.columns
df.columns.to_list()
df = df.drop(columns=['-'])

#%%

# Save down dataset 

df.to_csv('/content/drive/MyDrive/MMA Model/Data/ufcBouts_v6.csv')

#%%

# Create a unique model dataset! 

df_model = df.sample(frac=1).drop_duplicates(subset=['fight_link'])

df = df.drop_duplicates(subset='fighter_profile')

print(df)
# Explore the dataset 
print(df_model.columns)
# Columns in dataset 
print(df_model.shape[1]) # raw dataset should have 28 columns? 
# Unique fighters
print("Number of Unique Fighters: ", len(pd.unique(df_model['name'])))  # unique fighters
# Number of fights (nows in dataset)
print("Total Fights Recorded: ", len(df_model))
# Number of unique fights in the dataset 
print("Number of Unique Fights: ", len(pd.unique(df['fight_link'])))


df_model.to_csv('/content/drive/MyDrive/MMA Model/Data/ufcBouts_v6.csv')

# need to get age since fight 

# combine raw data with errata data (UFC stats)
# deal with birthdays / blanks 
# deal with event dates / blanks
 
# convert event dates
# find all upcoming events and delete? this should be based on dates

