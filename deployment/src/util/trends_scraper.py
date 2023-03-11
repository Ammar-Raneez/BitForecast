import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from util.mongodb import init_mongodb, TRENDS_COLLECTION

URL = 'https://bitinfocharts.com/comparison/google_trends-btc.html#alltime'

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
    Scrape URL script tag and extract trends & respective date
    '''

    dates = []
    trends = []

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
                trends.append(float(each))
            except:
                trends.append(None)

    return dates, trends

def create_dataframe():
    '''
    Create dataframe from scraped trends and dates
    '''

    dates, trends = process_scripts()
    df = pd.DataFrame(list(zip(dates, trends)), columns=['Date', 'bitcoin_unscaled'])
    return df

def export_data(df):
    '''
    Save data
    '''

    # Store datasets in mongodb for any requirements in production
    df.index = df.index.astype(str)
    df_dict = df.to_dict('index')
    dataset_db = init_mongodb()
    dataset_db[TRENDS_COLLECTION].delete_many({})
    dataset_db[TRENDS_COLLECTION].insert_one(df_dict)
    print('Saved data to MongoDB')

def update_trends():
    '''
    Main runner
    '''

    print('\nRunning Google Trends scraper...', end='\n')
    df = create_dataframe()
    export_data(df)
    print('\nGoogle Trends data updated', end='\n')

    # Return for script
    return df
