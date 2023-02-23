import sys
sys.path.append( '.' )

import numpy as np
import pandas as pd

import tensorflow as tf

from server.api.common import create_ensemble, get_upper_lower_bounds, load_ensemble, save_ensemble

HORIZON = 1
WINDOW_SIZE = 7
BATCH_SIZE = 1024
BTC_PRICES_DATA = 'D:/Uni/FYP/GitHub/BitForecast/ml/data/BTC_Prices.csv'
ENSEMBLE_PATH = 'D:/Uni/FYP/GitHub/BitForecast/server/models/ensemble_univariate_complete'

def get_future_dates(start_date, into_future, offset=1):
  '''
  Return dates from start_date to start_date + into_future
  Creates the dates of which the forecast was made
  '''

  start_date = start_date + np.timedelta64(offset, 'D')
  end_date = start_date + np.timedelta64(into_future, 'D')
  return np.arange(start_date, end_date, dtype='datetime64[D]')

def create_dataset():
  '''
  Create the required dataset format (Windowing, Cleaning & Spitting)
  '''

  # Import data
  data = pd.read_csv(BTC_PRICES_DATA)

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
  return data, y_all, dataset_all

def create_univariate_ensemble():
  '''
  Create the univariate ensemble model (for the case of retraining)
  '''

  _, _, dataset_all = create_dataset()
  ensemble = create_ensemble(dataset_all)
  save_ensemble(ensemble)
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

      print(f'Model {i} Predicting on:\n{last_window} -> Prediction: {future_pred}')

      # Update future forecast list
      model_forecast.append(future_pred)

      # Update last window: append latest and take last {WINDOW_SIZE} values
      last_window = np.append(last_window, future_pred)[-window_size:]

    future_forecast.append(model_forecast)

  return future_forecast

def forecast(into_future=5):
  '''
  Create the forecast
  '''

  raw_data, y_all, _ = create_dataset()
  ensemble = load_ensemble()

  future_forecast = make_future_forecasts(
    values=y_all,
    ensemble=ensemble,
    into_future=into_future,
    window_size=WINDOW_SIZE
  )

  last_timestep = raw_data.index[-1]
  last_price = raw_data['Price'][-1]

  next_time_steps = get_future_dates(
    start_date=raw_data.index[-1], 
    into_future=into_future
  )

  point_future = np.median(future_forecast, axis=0)
  lower_future, upper_future = get_upper_lower_bounds(future_forecast)

  next_time_steps = np.insert(next_time_steps, 0, last_timestep)
  point_future = np.insert(point_future, 0, last_price)
  lower_future = np.insert(lower_future, 0, last_price)
  upper_future = np.insert(upper_future, 0, last_price)

  return {
    'Predicted For': [str(date) for date in list(next_time_steps)],
    'Point Forecast': [str(price) for price in list(point_future)],
    'Lowerbound Forecast': [str(price) for price in list(lower_future)],
    'Upperbound Forecast': [str(price) for price in list(upper_future)],
  }