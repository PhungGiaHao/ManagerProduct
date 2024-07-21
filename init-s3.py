import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
LocalStackEndPoint = os.getenv("LocalStackEndPoint")

print(f"S3_BUCKET: {S3_BUCKET}, AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}, AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}, LocalStackEndPoint: {LocalStackEndPoint}")


s3_client = boto3.client(
    "s3",
    endpoint_url=LocalStackEndPoint,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Function to create S3 bucket if it doesn't exist
def create_bucket_if_not_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Error occurred: {e}")

print(f"Creating S3 bucket '{S3_BUCKET}' if it doesn't already exist.")
create_bucket_if_not_exists(S3_BUCKET)

