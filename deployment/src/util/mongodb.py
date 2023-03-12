import pymongo

import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGODB_URI')
DB_NAME = 'datasets'
BTC_PRICES_COLLECTION = 'Bitcoin Prices'
BLOCK_REWARD_COLLECTION = 'Block Reward'
TRENDS_COLLECTION = 'Google Trends'
TWITTER_SENTIMENTS_COLLECTION = 'Twitter Sentiments'
TWITTER_VOLUME_COLLECTION = 'Twitter Volume'
FINAL_DATASET_COLLECTION = 'Final Dataset'

def init_mongodb():
  client = pymongo.MongoClient(MONGO_URI)
  datasets_db = client[DB_NAME]
  return datasets_db
