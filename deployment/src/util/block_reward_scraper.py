import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from src.util.mongodb import init_mongodb, BLOCK_REWARD_COLLECTION

URL = 'https://bitinfocharts.com/comparison/fee_to_reward-btc.html#alltime'

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
    Scrape URL script tag and extract block reward & respective date
    '''

    dates = []
    sizes = []

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
                sizes.append(float(each))
            except:
                sizes.append(None)

    return dates, sizes

def create_dataframe():
    '''
    Create dataframe from scraped block reward sizes and dates
    '''

    dates, sizes = process_scripts()
    df = pd.DataFrame(list(zip(dates, sizes)), columns=['Date', 'Block Reward Size'])
    return df

def export_data(df):
    '''
    Save data
    '''

    # Store datasets in mongodb for any requirements in production
    df.index = df.index.astype(str)
    df_dict = df.to_dict('index')
    dataset_db = init_mongodb()
    dataset_db[BLOCK_REWARD_COLLECTION].delete_many({})
    dataset_db[BLOCK_REWARD_COLLECTION].insert_one(df_dict)
    print('Saved data to MongoDB')

def update_block_reward():
    '''
    Main runner
    '''

    print('\nRunning block reward scraper...', end='\n')
    df = create_dataframe()
    export_data(df)
    print('\nBlock reward data updated', end='\n')

    # Return for script
    return df
