import requests 
from bs4 import BeautifulSoup
import pandas as pd
import re

from src.util.mongodb import init_mongodb, TWITTER_VOLUME_COLLECTION

URL = 'https://bitinfocharts.com/comparison/bitcoin-tweets.html#alltime'

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
scripts = soup.find_all('script')

def parse(string_list):
    '''
    parse list of strings within the script tag
    [date, volume]
    '''

    clean = re.sub('[\[\],\s]', '', string_list)
    splitted = re.split("[\'\"]", clean)
    values_only = [s for s in splitted if s != '']
    return values_only

def process_scripts():
    '''
    Scrape URL script tag and extract tweet volume & respective date
    '''

    dates = []
    tweets = []

    for script in scripts:
        if 'd = new Dygraph(document.getElementById("container")' in script.text:
            str_lst = script.text
            str_lst = '[[' + str_lst.split('[[')[-1]
            str_lst = str_lst.split(']]')[0] +']]'
            str_lst = str_lst.replace('new Date(', '').replace(')', '')
            data = parse(str_lst)

    for each in data:
        if (data.index(each) % 2) == 0:
            dates.append(each)
        else:
            try:
                tweets.append(float(each))
            except:
                tweets.append(None)

    return dates, tweets

def create_dataframe():
    '''
    Create dataframe from scraped twitter volume and dates
    '''

    dates, tweets = process_scripts()
    df = pd.DataFrame(list(zip(dates, tweets)), columns=['Date', 'Tweet Volume'])
    return df

def export_data(df):
    '''
    Save data
    '''

    # Store datasets in mongodb for any requirements in production
    df.index = df.index.astype(str)
    df.sort_values(['Date'], inplace=True)
    df_dict = df.to_dict('index')
    dataset_db = init_mongodb()
    dataset_db[TWITTER_VOLUME_COLLECTION].delete_many({})
    dataset_db[TWITTER_VOLUME_COLLECTION].insert_one(df_dict)
    print('Saved data to MongoDB')

def update_tweet_volume():
    '''
    Main runner
    '''

    print('\nRunning twitter volume scraper...', end='\n')
    df = create_dataframe()
    export_data(df)
    print('\nTwitter volume updated', end='\n')

    # Return for script
    return df
