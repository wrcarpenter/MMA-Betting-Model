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

# %% 

# Add in "headless" browsing
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

#%%

driver.get('https://www.bestfightodds.com/fighters/Jose-Aldo-659') # example

# links = driver.find_elements(By.CLASS_NAME, "main-row")  # works

# use Selenium to open web pages
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
links = soup.find_all("a")

event_list = []
fighter_list = []
url_front_substring = 'https://www.bestfightodds.com'

for l in links:
    
    pagelink = str(l.get('href'))
    
    if '/events/' in pagelink:
        print(url_front_substring + pagelink)
        
    if '/fighters/' in pagelink:
        print(url_front_substring + pagelink)
        # to_append = 
    
    else:
        # skip all other links pulled
        continue


#%%

# References 
# https://selenium-python.readthedocs.io/locating-elements.html







