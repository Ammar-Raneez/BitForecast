import tensorflow as tf
import os

from server.utils.lts import LTSCell

ENSEMBLE_PATH = 'D:/Uni/FYP/GitHub/BitForecast/server/models/ensemble_univariate_complete'

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

def save_ensemble(ensemble):
  '''
  Save ensemble
  '''

  for i, model in enumerate(ensemble):
    model.save(f'{ENSEMBLE_PATH}/model_{i}')

def load_ensemble():
  '''
  Load ensemble
  '''

  ensemble = [tf.keras.models.load_model(f'{ENSEMBLE_PATH}/{model}') for model in os.listdir(ENSEMBLE_PATH)]
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

  return ensemble