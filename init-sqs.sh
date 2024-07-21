#!/bin/bash

until curl -s https://localhost.localstack.cloud:4566/_localstack/health | grep '"s3": "running"'; do
  echo "Waiting for LocalStack..."
  sleep 2
done

# Create SQS Queue
aws --endpoint-url=https://localhost.localstack.cloud:4566/ sqs create-queue --queue-name InventoryAlerts

echo "SQS Queue 'InventoryAlerts' created successfully."