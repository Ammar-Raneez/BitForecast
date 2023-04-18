from flask import abort, jsonify, make_response

from src.update_data import update_data

### cron to update data ###
def update_datasets():
  try:
    update_data()
    return {
      'output': 'Datasets updated',
      'status': 201
    }, 201
  except Exception as e:
    print(e)
    abort(make_response(jsonify(message='Something went wrong while updating the datasets through the cron job'), 500))

if __name__ == '__main__':
  update_datasets()
