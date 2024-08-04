"""
MMA Bout Update

"""
# Importing
import requests
import csv 
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import datetime
from datetime import date
from pytz import timezone
eastern = timezone('US/Eastern')
import threading 
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
cores = multiprocessing.cpu_count()

#%%
source = 'https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/ufcBouts_v20.csv' # raw data
df      = pd.read_csv(source, header=0)  # initial file
df_orig = df  # store down a copy for reference if need be

# Explore the dataset, you have all 
print(df.columns)
print(df.shape)
# tabulate DOB
print(df['dob'].value_counts())
# print(df['dob'].head(50))  # look at birthday variables
print("Unique Fighters: ", len(pd.unique(df['name'])))  # unique fighters 
print(df.loc[df['dob'] == '--', ['name', 'weight', 'reach']])
 
# test that both fighter and opponenet have same amount of blanks (or something is off in the data)
print(sum(df["fighter_result"] == "-"))
print(sum(df["opponent_result"] == "-"))

# create test data where fight result was blank
blank_results = df[df["fighter_result"] == "-"]

print(len(blank_results)) # this should match the number of blank results from before
print(blank_results["event_date"].value_counts()) # this is the true test ... all of these events should be somewhat recent

# Drop all the blank result fights from the data to refresh
df = df[df['fighter_result'] != "-"]
print(len(df) - len(df_orig)) # shows that these values were dropped out

#%%
new_data = []
cols              = pd.read_csv('https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/fight_columns.csv', header=0)
fighter_url_links = pd.read_csv('https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/fighterLinks.csv', header=0) # replace this to run different tests
# this should get all possible fighter url links on the UFC website
fighter_urls = collect_fighter_urls(fighter_url_links)
print("Fighter Links Total:" ,len(fighter_urls))     # 4,192 unique fighters

# Get all new data, scraping over every fighter listed on the site
new_data = collect_new_bouts(fighter_urls, new_data, df)
# Create a dataframe here
pd_new_data = pd.DataFrame(new_data, columns=['name', 'fighter_link', 'fight_link'])
# Scrape all new data
new_bout_data = collect_bout_data(pd_new_data)

# Update dataset and save it out
columns_list = list(cols.columns.values)
new_bout_data = pd.DataFrame(new_bout_data, columns= columns_list)
update_df = pd.concat([df, new_bout_data])

# Testing updated dataframe
print(len(update_df))
print(len(df) - len(update_df))

update_df['dob'] = update_df['dob'].replace("--","")
update_df['dob'] = pd.to_datetime(update_df['dob'])
update_df['event_date'] = pd.to_datetime(update_df['event_date'])
 
# Save out dataframe to drive
# update_df.to_excel('/content/drive/MyDrive/MMA Model/Data/ufcBouts_v17.xlsx')
update_df.to_csv('C:/Users/wcarp/OneDrive/Desktop/MMA Bout Model/Data/ufcBouts_v20.csv', index=False)


#%%
def collect_new_bouts(fighter_urls, new_data, df):

 for fighter_url in fighter_urls:

    fighter_page  = requests.get(fighter_url)
    fighter_soup  = BeautifulSoup(fighter_page.text, 'html.parser')
    name          = fighter_soup.find_all('span', {'class' : 'b-content__title-highlight'})
    fightLink  = 'http://ufcstats.com/fight-details/'     # UFC Fighter substring link
    fightLink2 = 'http://www.ufcstats.com/fight-details/' # Second link to capture "www"

    for item in name:
        fighterName = item.text.strip()

    findUrls = fighter_soup.find_all('a')

    urls = []
    for link in findUrls:
        pageLink = str(link.get('href'))
        urls.append(pageLink)

    fightUrls = []
    for theLink in urls:
      if (fightLink in theLink or fightLink2 in theLink) and theLink not in fightUrls:
          fightUrls.append(theLink)
      else: continue

    for fight_url in fightUrls:

      search_url = fight_url

      if 'www.' in fight_url:
        search_url = fight_url.replace("www.", "")

      if search_url not in df['fight_link'].unique():
        print("New Link:  ", fighterName, fight_url)
        new_info = [fighterName, fighter_url, fight_url]
        new_data.append(new_info)

 return new_data

# Searching for new urls
def collect_fighter_urls(fighter_url_links):

  fighter_urls = fighter_url_links.values.tolist()

  fighterUrls = []
  counter = 0

  for url_for_letter in fighter_urls:
    for link in url_for_letter:
      
      print("Parsing: ", link)

      fighter_list_page = requests.get(link)
      fighter_list_soup = BeautifulSoup(fighter_list_page.text, 'html.parser')
      fighterLink = 'http://ufcstats.com/fighter-details/' # UFC Fighter substring link
      fighter_findUrls = fighter_list_soup.find_all('a')

      fighter_urls = []
      for link in fighter_findUrls:
          pageLink = str(link.get('href'))
          fighter_urls.append(pageLink)

      for theLink in fighter_urls:
        if fighterLink in theLink:
          if theLink not in fighterUrls:
            fighterUrls.append(theLink)
            counter += 1
        else: continue

  return fighterUrls


# Scraping engine
def collect_bout_data(pd_new_data):

  new_bout_data = []
  print("Size of new bout list:  ", len(pd_new_data))
  count = 0

  for row in range(0, len(pd_new_data)):

    fighter_url = pd_new_data['fighter_link'].iloc[row]

    # create list for fighter details
    fighter_profile_base = []

    fighter_page  = requests.get(fighter_url)
    fighter_soup  = BeautifulSoup(fighter_page.text, 'html.parser')

    fighter_title = fighter_soup.find_all('li', {'class' : "b-list__box-list-item b-list__box-list-item_type_block"})
    name          = fighter_soup.find_all('span', {'class' : 'b-content__title-highlight'})
    nickName      = fighter_soup.find_all('p', {'class' : "b-content__Nickname"})

    for item in name:
      fighterName = item.text.strip()

    for item in nickName:
      nickname = item.text.strip()
      if nickname == '':
        nickname = '-'

    # Get basic fighter information, some info could be missing
    for item in fighter_title:

      word = item.text.strip()

      if 'Height:' in word:
          height = word.replace('Height:', '').strip()

      elif 'Weight:' in word:
          weight = word.replace('Weight:', '').strip()

      elif 'DOB:' in word:
          dob =    word.replace('DOB:', '').strip()
          # update the DOB format here
          if dob == '' or dob == ' ':
            dob = '-'

      elif 'STANCE' in word:
          stance = word.replace('STANCE:', '').strip()
          if stance == '' or stance ==' ':
            stance = '-'

      elif 'Reach:' in word:
          reach =  word.replace('Reach:', '').strip()
          if reach == '' or reach==' ':
            reach = '-'

      else:
        continue

    # Create base fighter profile
    fighter_profile_base.append(fighter_url)
    fighter_profile_base.append(fighterName)
    fighter_profile_base.append(nickname)
    fighter_profile_base.append(dob)
    fighter_profile_base.append(height)
    fighter_profile_base.append(weight)
    fighter_profile_base.append(reach)
    fighter_profile_base.append(stance)

    print('Adding new fight for: ', fighterName, "...Parsed: ", count, " / ", len(pd_new_data))

    count = count+1

    # get each fight URL from a fighter page
    fightLink  = 'http://ufcstats.com/fight-details/'     # UFC Fighter substring link
    fightLink2 = 'http://www.ufcstats.com/fight-details/' # Second link to capture "www"

    fight_row = []

    fight_url  = pd_new_data['fight_link'].iloc[row]

    fight_page = requests.get(fight_url)
    fight_soup = BeautifulSoup(fight_page.text, 'html.parser')

    event_title = fight_soup.find_all('h2', {'class' : 'b-content__title'})

    link_of_event = '-'
    event_date = '-'

    event_sublink1 = 'http://http://ufcstats.com/event-details/b0a6124751a56bc4'
    event_sublink2 = 'http://www.ufcstats.com/event-details/'
    event_sublink3 = 'ufcstats.com/event-details/'

    event_urls = fight_soup.find_all('a')

    for link in event_urls:
      pagelink = str(link.get('href'))

      if (event_sublink1 in pagelink or event_sublink2 in pagelink \
          or event_sublink3 in pagelink):

          link_of_event = pagelink
          event_page    = requests.get(link_of_event)
          event_soup    = BeautifulSoup(event_page.text, 'html.parser')
          event_details = event_soup.find_all('li', {'class' : 'b-list__box-list-item'})

          for detail in event_details:
            detail_text = detail.text.strip()
            if 'Date:' in detail_text:
                event_date = detail_text.replace('Date:', '').strip()
                # update the event date format here

    for item in event_title:
      event = item.text.strip()
      fight_row.append(fight_url)
      fight_row.append(event)

    fight_row.append(link_of_event)
    fight_row.append(event_date)

    fight_outcomes = fight_soup.find_all("div", {'class' : 'b-fight-details__person'})

    for fighter in fight_outcomes:
      opponent = False
      results = fighter.findAll('i')
      links   = fighter.findAll('a')

      for a in links:
            name = a.text.strip()
            if name != fighterName:
              opponent = True
              opponentName = name
              opponentLink = str(a.get('href'))

      for result in results:

          fight_result  = result.text.strip()

          if fight_result == "": fight_result = "-"

          if not opponent:
            fighter_result = fight_result
          else:
            opponent_result = fight_result

    fight_row.append(fighterName)
    fight_row.append(opponentName)
    fight_row.append(opponentLink)
    fight_row.append(fighter_result)
    fight_row.append(opponent_result)

    fight_title = fight_soup.find_all('i', {'class' : "b-fight-details__fight-title"})

    for item in fight_title:

      type_of_fight = item.text.strip()
      fight_row.append(type_of_fight)

      bonuses = item.findAll('img')
      belt,perf,fon,sub,ko = '-','-','-','-','-'

      for bonus in bonuses:
        if 'belt.png' in bonus['src']:  belt = 1
        if 'perf.png' in bonus['src']:  perf = 1
        if 'fight.png' in bonus['src']: fon  = 1
        if 'sub.png' in bonus['src']:   sub  = 1
        if 'ko.png' in bonus['src']:    ko   = 1

    fight_row.append(belt)
    fight_row.append(perf)
    fight_row.append(fon)
    fight_row.append(sub)
    fight_row.append(ko)

    # Fight statistics
    fight_table  = fight_soup.find_all(True, {'class' : ["b-fight-details__text-item", "b-fight-details__text-item_first"]})
    detail_section = False
    det = '-'
    method, round, time, timeFormat = '-', '-', '-', '-'

    # Basic fight summary statistics
    for item in fight_table:
        word = item.text.strip()
        word = ' '.join(word.split())
        if 'Method:' in word:
            method = word.replace('Method:', '').strip()
        if 'Round:' in word:
              round  = word.replace('Round:', '').strip()
        if 'Time:' in word:
              time   = word.replace('Time:', '').strip()
        if 'Time format:' in word:
              timeFormat = word.replace('Time format:', '').strip()

    fight_row.append(method)
    fight_row.append(round)
    fight_row.append(time)
    fight_row.append(timeFormat)

    fight_details  = fight_soup.find_all(True, {'class' : "b-fight-details__text"})

    details = '-'
    for item in fight_details:

      word = item.text.strip()
      word = ' '.join(word.split())

      if 'Details:' in word:
        details = ' '.join(word.split())
        details = details.replace('Details:', '')
        details = details.strip()

      else:
          details = '-'

    fight_row.append(details)

    full_row = fighter_profile_base + fight_row
    new_bout_data.append(full_row)

  return new_bout_data




