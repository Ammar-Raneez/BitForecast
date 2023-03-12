import boto3
import tempfile
import os

s3_client = boto3.client(
  's3',
  aws_access_key_id='AKIAYIIZ5ONJ2QHFZX5P',
  aws_secret_access_key='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'
)

def save_to_s3(ensemble, location):
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
        s3_client.upload_file(local_path, 'bitforecast-resources', s3_path)

    print('Model saved to S3\n')
