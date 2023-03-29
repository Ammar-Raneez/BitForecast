import sys
sys.path.insert(0, 'D:/Uni/FYP/GitHub/BitForecast/server')

from flask_cors import CORS
from flask_restful import Api
from flask import abort, Flask, jsonify, make_response, request

import pandas as pd

from scripts.update_data import update_data
from api.univariate import univariate_forecast, create_univariate_ensemble
from api.multivariate import multivariate_forecast, create_multivariate_ensemble

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
API = Api(app)

@app.route('/ping')
def hello():
  return {
    'output': 'BitForecast server is healthy',
    'status': 200
  }, 200

@app.route('/api/v1/models/get-metrics', methods=['GET'])
def get_metrics():
  multivariate_evaluation = pd.read_csv('D:/Uni/FYP/GitHub/BitForecast/ml/notebooks/model/data/multivariate_evaluation.csv')
  univariate_evaluation = pd.read_csv('D:/Uni/FYP/GitHub/BitForecast/ml/notebooks/model/data/univariate_evaluation.csv')

  try:
    univariate_mae, univariate_mse, univariate_rmse, univariate_mape, univariate_mase = univariate_evaluation['mae'], univariate_evaluation['mse'], univariate_evaluation['rmse'], univariate_evaluation['mape'], univariate_evaluation['mase']
    multivariate_mae, multivariate_mse, multivariate_rmse, multivariate_mape, multivariate_mase = multivariate_evaluation['mae'], multivariate_evaluation['mse'], multivariate_evaluation['rmse'], multivariate_evaluation['mape'], multivariate_evaluation['mase']

    univariate_metrics = {
      'Naive': { 'mae': univariate_mae[0], 'mse': univariate_mse[0], 'rmse': univariate_rmse[0], 'mape': univariate_mape[0], 'mase': univariate_mase[0] },
      'Ensemble': { 'mae': univariate_mae[1], 'mse': univariate_mse[1], 'rmse': univariate_rmse[1], 'mape': univariate_mape[1], 'mase': univariate_mase[1] }
    }

    multivariate_metrics = {
      'Naive': { 'mae': multivariate_mae[0], 'mse': multivariate_mse[0], 'rmse': multivariate_rmse[0], 'mape': multivariate_mape[0], 'mase': multivariate_mase[0] },
      'Ensemble': { 'mae': multivariate_mae[1], 'mse': multivariate_mse[1], 'rmse': multivariate_rmse[1], 'mape': multivariate_mape[1], 'mase': multivariate_mase[1] }
    }

    return {
      'output': {
        'univariate_metrics': univariate_metrics,
        'multivariate_metrics': multivariate_metrics
      },
      'status': 200
    }, 200
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while getting evaluation metrics'), 500))

@app.route('/api/v1/models/univariate', methods=['POST'])
def univariate():
  inputs = request.get_json()
  print(inputs)

  try:
    number_of_days = inputs['days']
    output = univariate_forecast(number_of_days)
    print(output)
    return {
      'output': output,
      'status': 200
    }, 200
  except KeyError as ke:
    print(ke)
    abort(make_response(jsonify(message='Days attribute is not missing'), 400))
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while forecasting'), 500))

@app.route('/api/v1/models/multivariate', methods=['POST'])
def multivariate():
  try:
    output = multivariate_forecast()
    print(output)
    return {
      'output': output,
      'status': 200
    }, 200
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while forecasting'), 500))

@app.route('/api/v1/models/univariate/update', methods=['POST'])
def update_univariate_model():
  try:
    update_data()
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the datasets'), 500))

  try:
    create_univariate_ensemble()
    return {
      'output': 'Univariate model updated',
      'status': 201
    }, 201
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the univariate model'), 500))

@app.route('/api/v1/models/multivariate/update', methods=['POST'])
def update_multivariate_model():
  try:
    update_data()
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the datasets'), 500))

  try:
    create_multivariate_ensemble()
    return {
      'output': 'Multivariate model updated',
      'status': 201
    }, 201
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the multivariate model'), 500))

@app.route('/api/v1/models/update', methods=['POST'])
def update_models():
  try:
    print('Updating univariate model...')
    create_univariate_ensemble()
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the univariate model'), 500))

  try:
    print('Updating multivariate model...')
    create_multivariate_ensemble()
    return {
      'output': 'Multivariate model updated',
      'status': 201
    }, 201
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the multivariate model'), 500))

@app.route('/api/v1/data/update', methods=['POST'])
def update_datasets():
  try:
    update_data()
    return {
      'output': 'Datasets updated',
      'status': 201
    }, 201
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the datasets'), 500))

if __name__ == '__main__':
  app.run()
