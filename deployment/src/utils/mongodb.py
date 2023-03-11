import pymongo

def init_mongodb():
  client = pymongo.MongoClient('mongodb+srv://Ammar:DhF6EUunp15ME6TK@bitforecast.ifghzuj.mongodb.net/test?authSource=admin&replicaSet=atlas-4w9tbc-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
  datasets_db = client['datasets']
  return datasets_db
