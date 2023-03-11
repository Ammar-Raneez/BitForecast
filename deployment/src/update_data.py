'''
This script will utilize the scrapers and the available scripts to update all
the available data being used and in turn create the updated final dataset 
'''

from util.price_scraper import update_prices
from util.block_reward_scraper import update_block_reward
from util.trends_scraper import update_trends
from util.tweet_volume_scraper import update_tweet_volume
from util.tweet_scraper import update_tweets
from util.create_dataset import create_final_dataset

def update_data():
  '''
  Update all the available data
  '''

  print('\nRunning data update script...', end='\n')
  prices = update_prices()
  block_reward = update_block_reward()
  tweet_volume = update_tweet_volume()
  trends = update_trends()
  tweets = update_tweets()

  create_final_dataset(prices, block_reward, trends, tweet_volume, tweets)

  print('\nData update script completed', end='\n')
  print('Data successfully saved into MongoDB')
