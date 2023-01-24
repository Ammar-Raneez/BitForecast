import requests 
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = 'https://bitinfocharts.com/comparison/bitcoin-tweets.html#alltime'
FILE_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/Tweets/BTC_Tweet_Volume.csv'

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
            tweets.append(each)

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

    df.to_csv(FILE_PATH)

def update_tweet_volume():
    '''
    Main runner
    '''

    print('\nRunning twitter volume scraper...', end='\n')
    df = create_dataframe()
    export_data(df)
    print('\nTwitter volume updated', end='\n')

if __name__ == '__main__':
    update_tweet_volume()
