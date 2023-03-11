'''
This script will utilize the scrapers and the available scripts to update all
the available data being used and in turn create the updated final dataset 
'''

import sys
sys.path.insert(0, 'D:/Uni/FYP/GitHub/BitForecast/server')

from utils.price_scraper import update_prices
from utils.block_reward_scraper import update_block_reward
from utils.trends_scraper import update_trends
from utils.tweet_volume_scraper import update_tweet_volume
from utils.tweet_scraper import update_tweets
from scripts.create_dataset import create_final_dataset

def update_data():
  '''
  Update all the available data
  '''

  print('\nRunning data update script...', end='\n')
  scripts = [
    update_prices,
    update_block_reward,
    update_tweet_volume,
    update_tweets,
    update_trends,
    create_final_dataset,
  ]

  for script in scripts:
    script()

  print('\nData update script completed', end='\n')

if __name__ == '__main__':
  update_data()
