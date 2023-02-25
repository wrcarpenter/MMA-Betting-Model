# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""

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

source = 'https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/ufcFights_sample.csv'
df     = pd.read_csv(source, header=0) 

print(df.columns)
print(df.shape)

# tabulate DOB
print(df['dob'].value_counts())

print(df['dob'].head(50))  # look at birthday variables
print(len(pd.unique(df['name'])))  # unique fighters 

print(df.loc[df['dob'] == '--', ['name', 'weight', 'reach']])


df = df[df['dob'] != "--"]  # drops missing birthdays from the data 
df['dob'] = df['dob'].replace(',', '', regex=True)  # replace commas 
df['dob_pandas'] = pd.to_datetime(df['dob'], format="%b %d %Y")


df['event_date'] = df['event_date'].replace(',', '', regex=True)  # replace commas 
df['event_date_new'] = pd.to_datetime(df['event_date'], format="%B %d %Y")

print(df[['event_date', 'event_date_new']])


df['age_at_bout'] = (df['event_date_new'] - df['dob_pandas']) / np.timedelta64(1, 'Y')

df['age_at_bout'].describe()  # get summary statistics of age at time of bout
print(df.loc[df['reach'] == '--', ['name', 'weight', 'reach']])
 



# need to get age since fight 

# combine raw data with errata data (UFC stats)
# deal with birthdays / blanks 
# deal with event dates / blanks
 




# convert event dates
# find all upcoming events and delete? this should be based on dates

