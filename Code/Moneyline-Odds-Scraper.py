"""
Moneyline Scraper - Mixed Martial Arts Contests

Creator:      Will Carpenter
Date Created: 08-25-23 

Description: Scraper for bestfightodds.com to compile historical data on 
MMA contest odds, including prop bets. Selenium is used to open webpages and
get page source HTML. 

"""
import requests
import csv 
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

#%%
# Add in "headless" browsing
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

#%% 
# Get link data 
source = 'https://raw.githubusercontent.com/wrcarpenter/MMA-Betting-Model/main/Data/odds-fighter-links.csv'  
df      = pd.read_csv(source, header=0) 
df_orig = df 
del source
fighter_list = df['link'].values.tolist()

#%%
# Aquire new fight links
new_links = []
len(fighter_list)
counter = 0 
      
for link in fighter_list: 
    
    counter += 1    
    print("Parsing:  ", link)
    print(counter)
    print(" ")
    
    driver.get(link)
    page_source = driver.page_source
    soup        = BeautifulSoup(page_source, 'lxml')
    links       = soup.find_all("a")
    url_string  = 'https://www.bestfightodds.com'
        
    for i in links:
        pagelink = str(i.get('href'))
        to_app   = url_string + pagelink
    
        if '/fighters/' in to_app:
            new_links.append(to_app)
    
for link in new_links:
    if link not in fighter_list:
        fighter_list.append(link)

            
#%%
# Export to excel
df_fighters = pd.DataFrame(fighter_list, columns = ['link'])
df_events   = pd.DataFrame(event_list, columns = ['link'])

df_fighters.to_csv('C:/Users/wcarp/OneDrive/Desktop/MMA Bout  Model/Data/odds-fighter-links.csv')
df_events.to_csv('C:/Users/wcarp/OneDrive/Desktop/MMA Bout  Model/Data/odds-event-links.csv')

#%%
# Testing link 

# https://www.bestfightodds.com/fighters/Wilson-Reis-710
ex = 'https://www.bestfightodds.com/fighters/Israel-Adesanya-7845'
ex = 'https://www.bestfightodds.com/fighters/Chris-Manuel-568'

driver.get(ex)
page_source = driver.page_source
soup        = BeautifulSoup(page_source, 'lxml')
events      = soup.find_all('a')
table       = soup.findAll('table')

for row in table:
    name     = row.find_all('th')   # but do not include "Matchup", etc. 
    row_data = row.find_all('td')
    
    # name, name link, open, closing range, movement, event name, event link, event date
    # Map with name, event date
    
    for data in name:
        print("------------------------")
        print(data.text.strip())
    
    for data in row_data:
        print("------------------------")
        print(data.text.strip())

for r in rows:
    name = r.findAll('')

# for each row:
# get the event name, link, date, fighter name, fighter link 
# get open, closing range, movement    
# keep the future events...but probably not that useful 
# fighter of focus is always first line 

#%% 
# References 
# https://selenium-python.readthedocs.io/locating-elements.html







