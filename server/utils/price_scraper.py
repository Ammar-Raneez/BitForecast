import requests
import json

prices = []
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

def export_data():
    '''
    Export obtained data as JSON
    '''
    json_data = json.dumps(prices, indent=4)
    with open ('../../data/prices.json', 'w') as file:
        file.write(json_data)

# API reference: http://api.scraperlink.com/investpy/