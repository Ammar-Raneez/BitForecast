'''
This script will utilize the scrapers and the available scripts to update all
the available data being used and in turn created the updated final dataset 
'''

import time

import sys
sys.path.append( '.' )

from server.utils.price_scraper import update_prices
from server.utils.block_reward_scraper import update_block_reward
from server.utils.gtrends_scraper import update_trends
from server.utils.tweet_volume_scraper import update_tweet_volume
from server.utils.tweet_scraper import update_tweets
from server.scripts.create_dataset import create_final_dataset

def update_data():
  '''
  Update all the available data
  '''

  print('\nRunning data update script...', end='\n')
  scripts = [
    update_prices,
    update_block_reward,
    update_trends,
    update_tweet_volume,
    update_tweets,
    create_final_dataset
  ]

  for script in scripts:
    script()
    time.sleep(2)

  print('\nData update script completed', end='\n')

if __name__ == '__main__':
  update_data()
