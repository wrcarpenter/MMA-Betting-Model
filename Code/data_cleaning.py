# MMA Bout Cleaning 
# W. Carpenter 

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
source = 'https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/ufcBouts_v20.csv'  
df      = pd.read_csv(source, header=0) 
df_orig = df # preserve a copy in case
del source

#%%
# Exploring the dataset quickly 
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
# Eliminate any missing DOB
df = df[df['dob'].notna()]     # drops missing birthdays from the data
df = df[df['height'] != "--"]  

print(len(df) - len(df_orig))  # drops 871 obs currently

df['dob'] = df['dob'].replace(',', '', regex=True)  # replace commas
df['dob'] = df['dob'].replace('--', '', regex=True)  # replace commas

df['event_date'] = pd.to_datetime(df['event_date'])
df['dob'] = pd.to_datetime(df['dob'])

df = df.sort_values(by=['fighter_profile', 'event_date'], ascending=True)
 
#%%
df['upcoming']    = np.where(df['fighter_result'] == "-" ,1, 0)
df['mens_bout']   = np.where(df['fight_type'].str.contains("Women"), 0, 1)
df['event_year']  = pd.DatetimeIndex(df['event_date']).year
# Current age of fighter at date time (years)
df['current_age'] = (df['event_date'] - df['dob']) / np.timedelta64(1, 'Y')

# Number of previous recorded fights in data 
df['ones'] = 1
df['prev_num_fights'] = df.groupby(['fighter_profile'])['ones'].cumsum() - 1

# Roster time
df['roster_start'] = df.groupby('fighter_profile')['event_date'].transform('min')
df['roster_time']  = (df['event_date'] - df['roster_start']) / np.timedelta64(1, "Y")

# Weeks since previous fight
# Weeks since will fill "N/A" if its the first fight in the dataset for a fighter
df['wks_since_last_fight'] = df.groupby(['fighter_profile'])['event_date'].diff()  
df['wks_since_last_fight'] = df['wks_since_last_fight'] / np.timedelta64(1, 'W')   

# Defining stance
df['stance_type'] = 0 # undefined
df.loc[df['stance'] == "Orthodox", 'stance_type'] = 1
df.loc[df['stance'] == "Southpaw", 'stance_type'] = 2
df.loc[df['stance'] == "Switch", 'stance_type']   = 3

#%%
# Make some adjustments via the date event to clean out some old fights
# drop all fights before 2011
df = df[df['event_year'] >= 2011]

# convert height to numerical 
df['feet']          = df['height'].str.slice(start=0, stop=1, step=1)
df['inches']        = df['height'].str.slice(start=2)
df['inches']        = df['inches'].replace('"','', regex=True)
df['height_inches'] = pd.to_numeric(df['feet'])*12 + pd.to_numeric(df['inches'])

#%% 
# Encoding some variables
df = df.rename(columns={'fight_type.1': 'time_format'})
df = df.rename(columns={'reach': 'reach_orig'})
df = df.rename(columns={'height': 'height_orig'})

df['reach_encode']   = df['reach_orig'].astype('category')
df['height_encode']  = df['height_orig'].astype('category') 

#%%  
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

# Breaking down decision results further
df['dec_split'] = df['method'].apply(lambda x: 1 if x == "Decision - Split" else 0)
df['dec_unani'] = df['method'].apply(lambda x: 1 if x == "Decision - Unanimous" else 0)

# Defining win categories for potential prediction 
df['ko_win']  = np.where(((df['ko']  == 1) & (df['win'] == 1)), 1, 0)
df['sub_win'] = np.where(((df['sub'] == 1) & (df['win'] == 1)), 1, 0) 
df['dec_win'] = np.where(((df['dec'] == 1) & (df['win'] == 1)), 1, 0) 

# What's next here 
# height,weight
# result of last fight (define categorical variables, ko_loss, ko_win, etc. )
# result of second to last fight

# Shifting for previous fight results 
# Issue here is that you are shifting up another fighters results to be the first observation!!!
# df.groupby('object')['value'].shift()

# write a function to handle previous fight results
# then build on this to figure out if any fighter was KO'd recently, etc.
    
# Should mark first fight, no previous data 
df['prev_fight_result'] = 0 

# Neither a win or loss
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['win'].shift(1) == 0)&\
                                    (df.groupby('fighter_profile')['loss'].shift(1) == 0 )),1,df['prev_fight_result'])
# Loss and KO result
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['loss'].shift(1) == 1)&\
                                    (df.groupby('fighter_profile')['ko'].shift(1) == 1 )),2,df['prev_fight_result'])    
# Loss and sub result
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['loss'].shift(1) == 1)&\
                                    (df.groupby('fighter_profile')['sub'].shift(1) == 1 )),3,df['prev_fight_result'])        
# Loss and dec result
df['prev_fight_result'] = np.where(((df.groupby('fighter_profile')['loss'].shift(1) == 1)&\
                                    (df.groupby('fighter_profile')['dec'].shift(1) == 1 )),4,df['prev_fight_result'])              

df['prev_fight_result'] = np.where(((df['dec_win'].shift(1) == 1)), 5, df['prev_fight_result'])
df['prev_fight_result'] = np.where(((df['sub_win'].shift(1) == 1)), 6, df['prev_fight_result'])
df['prev_fight_result'] = np.where(((df['ko_win'].shift(1) == 1)), 7, df['prev_fight_result'])

# Custom encoding 
# ko_win   = 7
# sub_win  = 6 
# dec_win  = 5
# dec_loss = 4
# sub_loss = 3 
# ko_loss  = 2
# other    = 1
# first    = 0

#%%
# "Browsing tools 
browse_columns = ['name', 'fighter_result', 'event_date', 'method', 'win', 'loss', 'ko', 'sub', 'dec','ko_win', 'prev_fight_result','sub_win', 'dec_win']

browse_columns = ['name', 'fighter_result', 'event_date', 'method']
# Browser for de-bugging 
df_browse = df[browse_columns]
df_browse_sample = df.loc[df['reach'] == '--', browse_columns]

# Very useful commands
df.columns
df.columns.to_list()
df = df.drop(columns=['-'])

#%%

# Mapping second fighter to first fighter (challenging)
# This is creating the opponent variables here 
# Map over age
# loop through each fight link in the column 
# get a datavalue 
# Helper variable for fighters 
# missing birthdays is creating issues here 

df['order'] = df.groupby(['fight_link'])['ones'].cumsum()
df = df.sort_values(by=['fight_link', 'order'], ascending=False)
df['drop'] = df.groupby(['fight_link'])['order'].cumsum()
# Dropping all single fight observations from dataset - these cannot be paired
df = df[df['drop'] != 1]
df = df.sort_values(by=['fight_link', 'order'], ascending=True)

# df['test'] = np.where(df['order'] == 1, 'one', 'zero')

# Mapping opponent variables to a given fight
df['opp_age']    = np.where(df['order'] == 1, df['age'].shift(-1), df['age'].shift(1))
df['opp_reach']  = np.where(df['order'] == 1, df['reach'].shift(-1), df['reach'].shift(1))
df['opp_height'] = np.where(df['order'] == 1, df['height_inches'].shift(-1), df['height_inches'].shift(1))
df['opp_stance'] = np.where(df['order'] == 1, df['stance_type'].shift(-1), df['stance_type'].shift(1))

# Clean up dataset
df = df.drop(columns=['feet', 'inches'])

df.to_excel('Downloads/ufcModel.xlsx')

#%%

# Create a unique model dataset 
df_model = df.sample(frac=1).drop_duplicates(subset=['fight_link'])
# df = df.drop_duplicates(subset='fighter_profile')
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

df_model.to_csv('Downloads/model_data.csv')

# Model dataset is then split into two parts (training and upcoming)





















