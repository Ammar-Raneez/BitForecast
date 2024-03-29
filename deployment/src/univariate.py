'''
This file handles univariate forecasting
'''

import numpy as np
import pandas as pd
import tensorflow as tf

import os

from src.update_data import update_data
from src.common import get_future_dates, check_data, get_upper_lower_bounds, save_ensemble, load_ensemble, create_ensemble
from src.util.mongodb import init_mongodb, BTC_PRICES_COLLECTION
from src.util.aws import save_to_s3

HORIZON = 1
WINDOW_SIZE = 7
BATCH_SIZE = 1024
ENSEMBLE_PATH = os.path.join(os.getcwd(), 'src', 'models', 'ensemble_univariate_complete')
ENSEMBLE_PATH = ENSEMBLE_PATH.replace('\\', '/')

def create_univariate_dataset():
  '''
  Create the required dataset format (Windowing, Cleaning & Spitting)
  '''

  # Import data from MongoDB
  db = init_mongodb()
  prices = db[BTC_PRICES_COLLECTION].find_one()
  del prices['_id']
  data = pd.DataFrame.from_dict(prices, orient='index')
  print('Data successfully imported from MongoDB\n')

  # Clean up data
  data.drop(['volume', 'open', 'max', 'min', 'change_percent'], axis=1, inplace=True)
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

def create_univariate_ensemble():
  '''
  Create the univariate ensemble model (for the case of retraining)
  '''

  data = create_univariate_dataset()

  # Update data if not up to date
  is_data_updated = check_data(data)
  if not is_data_updated:
    print('Data is not up to date, hence running update script first...\n')
    update_data()
  else:
    print('Data is up to date, hence skipping update script\n')

  ensemble = create_ensemble(data['dataset_all'])
  save_to_s3(ensemble, 'univariate_ensemble')
  save_ensemble(ensemble, ENSEMBLE_PATH)
  return ensemble

def make_future_forecasts(
  values,
  ensemble,
  into_future,
  window_size=WINDOW_SIZE
):
  '''
  Make future perdictions
  '''

  future_forecast = []

  # Predict {into_future} times with all models in the ensemble
  for i, model in enumerate(ensemble):
    model_forecast = []
    last_window = values[-window_size:] # last {WINDOW_SIZE} prices
    for _ in range(into_future):
      future_pred = tf.squeeze(
        model.predict(tf.expand_dims(last_window, axis=0))
      ).numpy()

      print(f'Model {i} -> Prediction: {future_pred}')

      # Update future forecast list
      model_forecast.append(future_pred)

      # Update last window: append latest and take last {WINDOW_SIZE} values
      last_window = np.append(last_window, future_pred)[-window_size:]

    future_forecast.append(model_forecast)

  return future_forecast

def univariate_forecast(into_future=5):
  '''
  Create the forecast
  '''

  print('Creating univariate dataset...\n')
  data = create_univariate_dataset()
  print('Univariate dataset created\n')

  print('Loading in model ensemble...\n')
  ensemble = load_ensemble(ENSEMBLE_PATH)
  print('Model ensemble loaded\n')

  print('Making forecast...\n')
  future_forecast = make_future_forecasts(
    values=data['y_all'],
    ensemble=ensemble,
    into_future=into_future,
    window_size=WINDOW_SIZE
  )
  print('Forecast created\n')

  # last_timestep = raw_data.index[-1]
  # last_price = raw_data['Price'][-1]

  print('Obtaining forecast timesteps...\n')
  next_time_steps = get_future_dates(
    start_date=data['data'].index[-1], 
    into_future=into_future
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
