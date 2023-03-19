import boto3
import tempfile

import os
from dotenv import load_dotenv
load_dotenv()

s3_client = boto3.client(
  's3',
  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def save_to_s3(ensemble, location):
  print('Running save ensemble to S3...\n')
  with tempfile.TemporaryDirectory() as temp_dir:
    print('Saving model to temporary directory...\n')
    for i, model in enumerate(ensemble):
      model.save(f'{temp_dir}/model_{i}')
    print('Model saved to temporary directory\n')

    print('Saving model to S3...\n')
    for root, _, files in os.walk(temp_dir):
      for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, temp_dir)
        s3_path = os.path.join(location, relative_path)

        # Required for Windows
        s3_path = s3_path.replace('\\', '/')
        s3_client.upload_file(local_path, os.getenv('AWS_BUCKET_NAME'), s3_path)

    print('Model saved to S3\n')

def read_model_from_bucket(location):
  '''
  NOTE
  This is going to make things extremely slow if we
  are to do this every time an inference is required.
  '''

  local_dir = 'src/models'
  if not os.path.exists(local_dir):
    os.makedirs(local_dir)

  response = s3_client.list_objects_v2(
    Bucket=os.getenv('AWS_BUCKET_NAME'),
    Prefix=location,
    Delimiter='/'
  )

  # This script is responsible for downloading the model into storage
  # Such a script is necessary as the savedModel format has nested folders
  for obj in response.get('Contents', []):
    s3_path = obj['Key']
    local_path = os.path.join(local_dir, os.path.relpath(s3_path, location))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3_client.download_file(os.getenv('AWS_BUCKET_NAME'), s3_path, local_path)
  for prefix in response.get('CommonPrefixes', []):
    subfolder = prefix['Prefix']
    local_subdir = os.path.join(local_dir, os.path.relpath(subfolder, location))
    os.makedirs(local_subdir, exist_ok=True)
    response = s3_client.list_objects_v2(Bucket=os.getenv('AWS_BUCKET_NAME'), Prefix=subfolder, Delimiter='/')
    for obj in response.get('Contents', []):
        s3_path = obj['Key']
        local_path = os.path.join(local_dir, os.path.relpath(s3_path, location))
        s3_client.download_file(os.getenv('AWS_BUCKET_NAME'), s3_path, local_path)
    for subprefix in response.get('CommonPrefixes', []):
        subsubfolder = subprefix['Prefix']
        local_subsubdir = os.path.join(local_dir, os.path.relpath(subsubfolder, location))
        os.makedirs(local_subsubdir, exist_ok=True)
        response = s3_client.list_objects_v2(Bucket=os.getenv('AWS_BUCKET_NAME'), Prefix=subsubfolder, Delimiter='/')
        for obj in response.get('Contents', []):
            s3_path = obj['Key']
            local_path = os.path.join(local_dir, os.path.relpath(s3_path, location))
            s3_client.download_file(os.getenv('AWS_BUCKET_NAME'), s3_path, local_path)
