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
ex = 'https://www.bestfightodds.com/fighters/Zelim-Imadaev-8102'

ex = 'https://www.bestfightodds.com/fighters/Ronda-Rousey-2741'

driver.get(ex)
page_source = driver.page_source
soup        = BeautifulSoup(page_source, 'lxml')
events      = soup.find_all('a')
table       = soup.findAll('table')
# empty list
# name, name link, open, closing range, movement, event name, event link, event date 

page_table = []


for row in table: 
    
    # Compile various page data  
    links  = row.find_all('a')                              # contains links, names, and event names
    name   = row.find_all('th', {'class' : "oppcell"})      # find names
    mline  = row.find_all('td', {'class' : "moneyline"})    # find moneylines
    move   = row.find_all('td', {'class' : "change-cell"})  # moneyline vol
    event  = row.find_all('tr', {'class' : "event-header item-mobile-only-row" }) # event dates

    # and now you fill in each row 
    
    # name, link, event, date, event_link, open, close left, close right, movement % (if applicable)
    print(len(links)) # there are double the amount of links 
    print(len(name))
    print(len(event))
    print(len(mline)) # this will be difficult to implement 
    
    
    for data in move:
        print("------------------------")
        mstring = data.text.strip()
        mstring = mstring.replace("▲", '')
        mstring = mstring.replace('▼', '')
        print(mstring)
    
    # create a row
    date_index = 0
      
    for i in range(0, len(name)):
        
        page_row =[]
        
        app_name    = name[i].text.strip()
        app_event   = str(links[i*2].get('href'))
        app_profile = str(links[i*2+1].get('href'))
        
        event_date =  event[date_index].text.strip()
        event_date =  event_date.split()
        event_date =  event_date[-3] + ' ' + event_date[-2] + ' ' + event_date[-1]
        if i % 2 != 0: date_index += 1
        
        app = [app_name, app_event, app_profile, event_date]
        page_row.extend(app)

        
                
        page_table.append(page_row)
    

page_data = pd.DataFrame(page_table)        

#%% 
# References 
# https://selenium-python.readthedocs.io/locating-elements.html







