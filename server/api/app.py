from flask_cors import CORS
from flask_restful import Api
from flask import Flask, request

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
API = Api(app)

@app.route('/')
def hello():
  return 'Hello, World!'

@app.route('/api/v1/models/univariate', methods=['POST'])
def univariate():
  inputs = request.get_json()
  print(inputs)
  return 'Univariate API'

@app.route('/api/v1/models/multivariate', methods=['POST'])
def multivariate():
  inputs = request.get_json()
  print(inputs)
  return 'Multivariate API'

if __name__ == '__main__':
  app.run()
