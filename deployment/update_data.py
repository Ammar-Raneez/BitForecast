'''
This script will utilize the scrapers and the available scripts to update all
the available data being used and in turn create the updated final dataset 
'''

from price_scraper import update_prices
from block_reward_scraper import update_block_reward
from gtrends_scraper import update_trends
from tweet_volume_scraper import update_tweet_volume
from tweet_scraper import update_tweets
from create_dataset import create_final_dataset

def update_data():
  '''
  Update all the available data
  '''

  print('\nRunning data update script...', end='\n')
  prices = update_prices()
  block_reward = update_block_reward()
  tweet_volume = update_tweet_volume()
  tweets = update_tweets()
  trends = update_trends()
  create_final_dataset(prices, block_reward, trends, tweet_volume, tweets)

  print('\nData update script completed', end='\n')

if __name__ == '__main__':
  update_data()
