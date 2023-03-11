import requests
import pandas as pd
from datetime import datetime

# API reference: http://api.scraperlink.com/investpy/
BASE_URL = 'http://api.scraperlink.com/investpy/?email=ammarraneez@gmail.com&type=historical_data&product=cryptos&symbol=BTC&key=474f2c8d88ee117dc1408e97d03c6a24a745db9c'
FILE_PATH = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/BTC_Prices.csv'

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
    # df.set_index('date', inplace=True)
    return df

def export_data(df):
    '''
    Save data
    '''

    df.to_csv(FILE_PATH)

def update_prices():
    '''
    Main runner
    '''

    print('\nRunning historical prices scraper...', end='\n')
    today = datetime.now().strftime('%m/%d/%Y')
    prices = get_crypto_data('01/01/2014', today)
    df = clean_data(prices)
    export_data(df)
    print('\nHistorical prices data updated', end='\n')

    # Return for script
    return df

if __name__ == '__main__':
    update_prices()
