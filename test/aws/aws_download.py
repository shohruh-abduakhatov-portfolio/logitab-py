import boto3
from botocore.client import Config


FILE_NAME = 'large.png'

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'logitab-signature'

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

# Image download
s3.Bucket(BUCKET_NAME).download_file(FILE_NAME, '_large.png')  # Change the second part
# This is where you want to download it too.

print("Done")
