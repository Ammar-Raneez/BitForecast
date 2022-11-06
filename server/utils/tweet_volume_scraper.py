import requests 
from bs4 import BeautifulSoup
import pandas as pd
import re

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
    dates, tweets = process_scripts()
    df = pd.DataFrame(list(zip(dates, tweets)), columns=['Date', 'Tweet Volume'])
    return df

def export_data(df):
    df.to_csv('../../data/BTC_Tweet_Volume.csv')





