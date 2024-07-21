import logging
import boto3
from botocore.exceptions import NoCredentialsError
import json
import os
from dotenv import load_dotenv
load_dotenv()


LocalStackEndPoint = os.getenv("LocalStackEndPoint")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

dynamodb = boto3.client(
    'dynamodb',
    endpoint_url=LocalStackEndPoint,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def create_table():
    try:
        dynamodb.create_table(
            TableName='ApiCallTracking',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table created successfully.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

def log_api_call(call_id, timestamp, method, path, status_code, process_time):
    dynamodb.put_item(
        TableName='ApiCallTracking',
        Item={
            'id': {'S': call_id},
            'timestamp': {'S': timestamp},
            'method': {'S': method},
            'path': {'S': path},
            'status_code': {'N': str(status_code)},
            'process_time': {'N': str(process_time)}
        }
    )