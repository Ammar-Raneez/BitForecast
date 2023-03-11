import pymongo

MONGO_URI = 'mongodb+srv://Ammar:DhF6EUunp15ME6TK@bitforecast.ifghzuj.mongodb.net/test?authSource=admin&replicaSet=atlas-4w9tbc-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'
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
