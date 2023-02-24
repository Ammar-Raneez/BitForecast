from flask_cors import CORS
from flask_restful import Api
from flask import abort, Flask, jsonify, make_response, request

import sys
sys.path.append( '.' )

from server.scripts.update_data import update_data
from server.api.univariate import univariate_forecast, create_univariate_ensemble
from server.api.multivariate import multivariate_forecast, create_multivariate_ensemble

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
