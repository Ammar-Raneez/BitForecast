'''
This file fetches the historical prices required by the forecasting model
'''

import requests
import pandas as pd
from datetime import datetime

from src.util.mongodb import init_mongodb, BTC_PRICES_COLLECTION

# API reference: http://api.scraperlink.com/investpy/
BASE_URL = 'http://api.scraperlink.com/investpy/?email=ammarraneez@gmail.com&type=historical_data&product=cryptos&symbol=BTC'

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
    '''
    Create dataframe of fetched prices
    '''

    return pd.DataFrame(prices)

def clean_data(prices):
    '''
    Clean data and remove unneeded columns
    '''

    df = create_dataframe(prices)
    df.drop(['direction_color', 'rowDateRaw', 'last_close', 'last_open', 'last_max', 'last_min', 'volume', 'change_precent'], axis=1, inplace=True)
    df.rename(columns={ 'volumeRaw': 'volume', 'last_closeRaw': 'close', 'last_openRaw': 'open', 'last_maxRaw': 'max', 'last_minRaw': 'min', 'change_precentRaw': 'change_percent' }, inplace=True)
    df['date'] = pd.to_datetime(df['rowDate'])
    df.drop(['rowDate', 'rowDateTimestamp'], axis=1, inplace=True)
    df.sort_values(['date'], inplace=True)
    df['date'] = df['date'].astype(str)
    df['close'] = df['close'].astype(float)
    # df.set_index('date', inplace=True)
    return df

def export_data(df):
    '''
    Save data
    '''

    # Store datasets in mongodb for any requirements in production
    df.index = df.index.astype(str)
    df.sort_values(['date'], inplace=True)
    df_dict = df.to_dict('index')
    dataset_db = init_mongodb()
    dataset_db[BTC_PRICES_COLLECTION].delete_many({})
    dataset_db[BTC_PRICES_COLLECTION].insert_one(df_dict)
    print('Saved data to MongoDB\n')

def update_prices():
    '''
    Main runner
    '''

    print('Running historical prices scraper...\n')
    today = datetime.now().strftime('%m/%d/%Y')
    prices = get_crypto_data('01/01/2014', today)
    df = clean_data(prices)
    export_data(df)
    print('Historical prices data updated\n')

    # Return for script
    return df
