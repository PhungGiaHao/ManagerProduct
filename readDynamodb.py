import boto3
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
LocalStackEndPoint = os.getenv("LocalStackEndPoint")
# Initialize the DynamoDB client
dynamodb = boto3.client(
    'dynamodb',
    endpoint_url=LocalStackEndPoint,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

# Function to scan a table
def scan_table(table_name):
    response = dynamodb.scan(TableName=table_name)
    items = response.get('Items', [])
    return items

# Scan and print items from the ApiCallTracking table
items = scan_table('ApiCallTracking')
for item in items:
    print(item)