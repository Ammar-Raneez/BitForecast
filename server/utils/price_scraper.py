import requests
import json
import pandas as pd

# API reference: http://api.scraperlink.com/investpy/
BASE_URL = 'http://api.scraperlink.com/investpy/?email=your@email.com&type=historical_data&product=cryptos&symbol=BTC'
    
def get_crypto_data(start, end):
    '''
    Scrape data current solution
    Possible to break in future, therefore must create a dedicated scraper, if time permits
    '''
    response = requests.request(
        'GET',
        f'{BASE_URL}&from_date={start}&to_date={end}'
    )
    return response.json()['data']

def create_dataframe(prices):
    return pd.DataFrame(prices)

def export_data(df):
    df.to_csv('../../data/BTC_Prices.csv')
