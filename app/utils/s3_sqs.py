import logging
import boto3
from botocore.exceptions import NoCredentialsError
import json
import os
from dotenv import load_dotenv
load_dotenv()
from app.Routers.product import search_inventory

endpoint_url = os.getenv("sqs_url")
sqs_name = os.getenv("sqs_name")
LocalStackEndPoint = os.getenv("LocalStackEndPoint")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
sqs_client = boto3.client(
    'sqs',
    endpoint_url=LocalStackEndPoint,  # LocalStack endpoint
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def send_message_to_sqs(message_body: str):
    try:
        sqs_client.send_message(
            QueueUrl=endpoint_url,
            MessageBody=message_body
        )
        print("Message sent to SQS")
    except NoCredentialsError:
        print("Credentials not available")


def read_messages_from_sqs():
    try:
        response = sqs_client.receive_message(
            QueueUrl=endpoint_url,
            MaxNumberOfMessages=10,  # Number of messages to receive
            WaitTimeSeconds=10  # Long polling wait time
        )
        messages = response.get('Messages', [])
        return messages
    except NoCredentialsError:
        print("Credentials not available")
        return []

def delete_message_from_sqs(receipt_handle: str):
    try:
        sqs_client.delete_message(
            QueueUrl=endpoint_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from SQS")
    except NoCredentialsError:
        print("Credentials not available")




## search db for product investory < 100 and send messages
def send_message_low_stock():
    try:
        logging.info("Sending low stock messages")
        low_stock_products = search_inventory()
        if len(low_stock_products) == 0:
            print("No low stock products found.")
            return
        for product in low_stock_products:
            message = f"Product {product.name} is low in stock. Current stock : {product.inventory}"
            print(f"Sending message: {message}")
            send_message_to_sqs(message)
    except Exception as e:
        print(f"Error occurred: {e}")
