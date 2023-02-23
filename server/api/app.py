from flask_cors import CORS
from flask_restful import Api
from flask import abort, Flask, jsonify, make_response, request

import sys
sys.path.append( '.' )

from server.scripts.update_data import update_data
from server.api.univariate import forecast, create_univariate_ensemble

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
API = Api(app)

@app.route('/ping')
def hello():
  return 'Hello, World!'

@app.route('/api/v1/models/univariate', methods=['POST'])
def univariate():
  inputs = request.get_json()
  print(inputs)

  try:
    number_of_days = inputs['days']
    output = forecast(number_of_days)
    print(output)
    return {
      'output': output,
      'status': 200
    }
  except KeyError:
    abort(make_response(jsonify(message='Days attribute is not missing'), 400))
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while forecasting'), 500))

@app.route('/api/v1/models/multivariate', methods=['POST'])
def multivariate():
  inputs = request.get_json()
  print(inputs)
  return 'Multivariate API'

@app.route('/api/v1/models/update', methods=['GET'])
def update_model():
  try:
    create_univariate_ensemble()
    return {
      'output': 'Model updated',
      'status': 200
    }
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the model'), 500))

@app.route('/api/v1/data/update', methods=['GET'])
def update_datasets():
  try:
    update_data()
    return {
      'output': 'Datasets updated',
      'status': 200
    }
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the datasets'), 500))

if __name__ == '__main__':
  app.run()
