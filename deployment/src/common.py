'''
This file contains common utility functions that are used in multivariate.py and univariate.py
'''

import numpy as np
import pandas as pd
import tensorflow as tf
import os
import datetime

from src.util.lts import LTSCell

MULTIVARIATE_EVALUATION_PATH = os.path.join(os.getcwd(), 'src', 'models', 'multivariate_evaluation.csv')
MULTIVARIATE_EVALUATION_PATH = MULTIVARIATE_EVALUATION_PATH.replace('\\', '/')

UNIVARIATE_EVALUATION_PATH = os.path.join(os.getcwd(), 'src', 'models', 'univariate_evaluation.csv')
UNIVARIATE_EVALUATION_PATH = UNIVARIATE_EVALUATION_PATH.replace('\\', '/')

def get_future_dates(start_date, into_future, offset=1):
  '''
  Return dates from start_date to start_date + into_future
  Creates the dates of which the forecast was made
  '''

  start_date = start_date + np.timedelta64(offset, 'D')
  end_date = start_date + np.timedelta64(into_future, 'D')
  return np.arange(start_date, end_date, dtype='datetime64[D]')

def check_data(data):
  '''
  Check if available data is up to date
  '''

  print('Checking if data is up to date...\n')
  today =  datetime.datetime.today().strftime('%Y-%m-%d')
  avail_date = data['data'].index[-1].strftime('%Y-%m-%d')
  print('Todays date: ', today, end='\n\n')
  print('Available date: ', avail_date, end='\n\n')
  return today == avail_date

def get_upper_lower_bounds(preds):
  '''
  Create prediction uncertainty estimates, for range prediction
  '''

  std = tf.math.reduce_std(preds, axis=0)

  # 1.96 is the 97.5th percentile point
  interval = 1.96 * std
  preds_mean = tf.reduce_mean(preds, axis=0)
  lower, upper = preds_mean - interval, preds_mean + interval
  return lower, upper

def save_ensemble(ensemble, path):
  '''
  Save ensemble locally
  Not used in deployment
  '''

  print('Saving ensemble locally...\n')
  for i, model in enumerate(ensemble):
    model.save(f'{path}/model_{i}')
  print('Ensemble saved locally\n')

def load_ensemble(path):
  '''
  Load ensemble from local
  Not used in deployment
  '''

  ensemble = [tf.keras.models.load_model(f'{path}/{model}') for model in os.listdir(path)]
  return ensemble

def create_ensemble(
  dataset_all,
  num_models=10,
  num_epochs=5000,
  window_size=7,
  horizon=1,
  loss_fns=['mae', 'mse', 'mape']
):
  '''
  Create an ensemble model (for the case of retraining)
  '''

  ensemble = []

  print('Creating ensemble...\n')
  for i in range(num_models):
    for loss_fn in loss_fns:
      print(f'Model loss: {loss_fn} | model number: {i}')
      model = tf.keras.Sequential([
        tf.keras.layers.Input(
          shape=(window_size)
        ),
        tf.keras.layers.Lambda(
          lambda x: tf.expand_dims(x, axis=1)
        ),
        tf.keras.layers.RNN(
          LTSCell(16),
          time_major=True,
          return_sequences=True
        ),
        tf.keras.layers.LSTM(
          16,
          activation='relu'
        ),
        tf.keras.layers.Dense(
          128,
          kernel_initializer='he_normal',       #Required for the prediction intervals
          activation='relu'
        ),
        tf.keras.layers.Dense(
          128,
          kernel_initializer='he_normal',
          activation='relu'
        ),
        tf.keras.layers.Dense(horizon)
      ])

      model.compile(
        loss=loss_fn,
        optimizer=tf.keras.optimizers.Adam(),
        metrics=['mae', 'mse']
      )

      model.fit(
        dataset_all,
        epochs=num_epochs,
        verbose=0,
      )

      ensemble.append(model)

  print('Ensemble created\n')
  return ensemble

def get_evaluation_results():
  '''
  Get the evaluation results of the ensemble model in use
  '''

  multivariate_evaluation = pd.read_csv(MULTIVARIATE_EVALUATION_PATH)
  univariate_evaluation = pd.read_csv(UNIVARIATE_EVALUATION_PATH)

  univariate_mae, univariate_mse, univariate_rmse, univariate_mape, univariate_mase = univariate_evaluation['mae'], univariate_evaluation['mse'], univariate_evaluation['rmse'], univariate_evaluation['mape'], univariate_evaluation['mase']
  multivariate_mae, multivariate_mse, multivariate_rmse, multivariate_mape, multivariate_mase = multivariate_evaluation['mae'], multivariate_evaluation['mse'], multivariate_evaluation['rmse'], multivariate_evaluation['mape'], multivariate_evaluation['mase']

  univariate_metrics = {
    'Naive': { 'mae': round(univariate_mae[0], 3), 'mse': round(univariate_mse[0], 3), 'rmse': round(univariate_rmse[0], 3), 'mape': f'{round(float(univariate_mape[0][:-1]), 3)}%', 'mase': round(univariate_mase[0], 3) },
    'Ensemble': { 'mae': round(univariate_mae[1], 3), 'mse': round(univariate_mse[1], 3), 'rmse': round(univariate_rmse[1], 3), 'mape': f'{round(float(univariate_mape[1][:-1]), 3)}%', 'mase': round(univariate_mase[1], 3) },
  }

  multivariate_metrics = {
    'Naive': { 'mae': round(multivariate_mae[0], 3), 'mse': round(multivariate_mse[0], 3), 'rmse': round(multivariate_rmse[0], 3), 'mape': f'{round(float(multivariate_mape[0][:-1]), 3)}%', 'mase': round(multivariate_mase[0], 3) },
    'Ensemble': { 'mae': round(multivariate_mae[1], 3), 'mse': round(multivariate_mse[1], 3), 'rmse': round(multivariate_rmse[1], 3), 'mape': f'{round(float(multivariate_mape[1][:-1]), 3)}%', 'mase': round(multivariate_mase[1], 3) },
  }

  return univariate_metrics, multivariate_metrics
