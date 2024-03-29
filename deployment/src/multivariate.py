'''
This file handles multivariate forecasting
'''

import numpy as np
import pandas as pd
import tensorflow as tf

import os

from src.update_data import update_data
from src.common import get_future_dates, check_data, get_upper_lower_bounds, save_ensemble, load_ensemble, create_ensemble
from src.util.mongodb import init_mongodb, FINAL_DATASET_COLLECTION
from src.util.aws import save_to_s3

HORIZON = 1
WINDOW_SIZE = 7
BATCH_SIZE = 1024
ENSEMBLE_PATH = os.path.join(os.getcwd(), 'src', 'models', 'ensemble_multivariate_complete')
ENSEMBLE_PATH = ENSEMBLE_PATH.replace('\\', '/')

def create_multivariate_dataset():
  '''
  Create the required dataset format (Windowing, Cleaning & Spitting)
  '''

  # Import data from MongoDB
  db = init_mongodb()
  prices = db[FINAL_DATASET_COLLECTION].find_one()
  del prices['_id']
  data = pd.DataFrame.from_dict(prices, orient='index')
  print('Data successfully imported from MongoDB\n')

  # Clean up data
  data = data[['date', 'volume', 'close', 'change_percent', 'Block Reward Size', 'bitcoin_unscaled', 'Tweet Volume', 'compound_score']]
  data['date'] = pd.to_datetime(data['date'])
  data.set_index('date', inplace=True)
  data.rename(columns={ 'close': 'Price' }, inplace=True)

  # Create window datasets
  data_windowed = data.copy()
  for i in range(WINDOW_SIZE):
    data_windowed[f'Price+{i+1}'] = data_windowed['Price'].shift(periods=i+1)

  # Create X and y
  x_all = data_windowed.dropna().drop('Price', axis=1).astype(np.float32)
  y_all = data_windowed.dropna()['Price'].astype(np.float32)

  # Convert tensorflow datasets
  features_dataset_all = tf.data.Dataset.from_tensor_slices(x_all)
  labels_dataset_all = tf.data.Dataset.from_tensor_slices(y_all)
  dataset_all = tf.data.Dataset.zip((features_dataset_all, labels_dataset_all))
  dataset_all = dataset_all.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

  return {
    'data': data,
    'data_windowed': data_windowed,
    'y_all': y_all,
    'x_all': x_all,
    'dataset_all': dataset_all,
  }

def create_multivariate_ensemble():
  '''
  Create the multivariate ensemble model (for the case of retraining)
  '''

  data = create_multivariate_dataset()
  # Update data if not up to date
  is_data_updated = check_data(data)
  if not is_data_updated:
    print('Data is not up to date, hence running update script first...\n')
    update_data()
  else:
    print('Data is up to date, hence skipping update script\n')

  ensemble = create_ensemble(data['dataset_all'])
  save_to_s3(ensemble, 'multivariate_ensemble')
  save_ensemble(ensemble, ENSEMBLE_PATH)
  return ensemble

def make_future_forecasts(
  values,
  ensemble,
  window_size=WINDOW_SIZE
):
  '''
  Make future perdiction
  '''

  future_forecast = []

  for i, model in enumerate(ensemble):
    last_window = values[-window_size:] # last {WINDOW_SIZE} prices
    future_pred = tf.squeeze(
      model.predict(last_window)
    ).numpy()[-1]

    print(f'Model {i} -> Prediction: {future_pred}')
    future_forecast.append([future_pred])

  return future_forecast

def multivariate_forecast():
  '''
  Create the forecast
  '''

  print('Creating multivariate dataset...\n')
  data = create_multivariate_dataset()
  print('Multivariate dataset created\n')

  print('Loading in model ensemble...\n')
  ensemble = load_ensemble(ENSEMBLE_PATH)
  print('Model ensemble loaded\n')

  print('Making forecast...\n')
  future_forecast = make_future_forecasts(
    values=data['x_all'],
    ensemble=ensemble,
    window_size=WINDOW_SIZE
  )
  print('Forecast created\n')

  # last_timestep = data['data'].index[-1]
  # last_price = data['data']['Price'][-1]

  print('Obtaining forecast timesteps...\n')
  next_time_steps = get_future_dates(
    start_date=data['data'].index[-1], 
    into_future=1
  )
  print('Forecast timesteps obtained\n')

  print('Obtaining forecast and bounds...\n')
  point_future = np.median(future_forecast, axis=0)
  lower_future, upper_future = get_upper_lower_bounds(future_forecast)
  print('Forecast and bounds obtained\n')

  # Only needed when joining the graph lines
  # next_time_steps = np.insert(next_time_steps, 0, last_timestep)
  # point_future = np.insert(point_future, 0, last_price)
  # lower_future = np.insert(lower_future, 0, last_price)
  # upper_future = np.insert(upper_future, 0, last_price)

  return {
    'Predicted For': [str(date) for date in list(next_time_steps)],
    'Point Forecast': [str(price) for price in list(point_future)],
    'Lowerbound Forecast': [str(price.numpy()) for price in list(lower_future)],
    'Upperbound Forecast': [str(price.numpy()) for price in list(upper_future)],
  }
