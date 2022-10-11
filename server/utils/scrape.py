import requests
import json

class Scraper:
    def __init__(self):
        self._prices = []
        self._BASE_URL = 'http://api.scraperlink.com/investpy/?email=your@email.com&type=historical_data&product=cryptos&symbol=BTC'
    
    def get_crypto_data(self, start, end):
        '''
        Scrape data current solution
        Possible to break in future, therefore must create a dedicated scraper, if time permits
        '''
        response = requests.request(
            'GET',
            f'{self._BASE_URL}&from_date={start}&to_date={end}'
        )
        self._prices = response.json()['data']

    def get_prices(self):
        '''
        Returns the obtained prices from the API
        '''
        return self._prices
        
    def export_data(self):
        '''
        Export obtained data as JSON so it can be used by the model
        '''
        json_data = json.dumps(self._prices, indent=4)
        with open ('prices.json', 'w') as file:
            file.write(json_data)
        
# API reference: http://api.scraperlink.com/investpy/
