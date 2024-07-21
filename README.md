# FastAPI Backend API Project

## Overview

This project is a backend API built with FastAPI, demonstrating integration with various AWS services and databases. It uses both SQL and NoSQL databases, and incorporates AWS Lambda, DynamoDB, S3, and SQS/EventBridge.

## Technical Requirements

- **Python**: The programming language used for development.
- **Docker**: Containerization tool for managing dependencies and deployment.
- **SQL Database**: PostgreSQL for the main database.
- **NoSQL Database**: DynamoDB for tracking API calls.
- **AWS Lambda**: Serverless compute service for executing code in response to events.
- **DynamoDB**: Managed NoSQL database for storing and querying data.
- **S3**: Object storage service for storing files.
- **SQS/EventBridge**: Messaging and event bus services for managing asynchronous workflows.
- **Boto3**: AWS SDK for Python to interact with AWS services.
- **Unit Testing**: pytest for writing and running tests.

## Setup and Installation

### 1. **Clone the Repository**
 ```bash
git clone https://github.com/your-username/your-repository.git](https://github.com/PhungGiaHao/ManagerProduct.git)
cd your-repository
pip install -r requirements.txt
```
### 2. **Set Up Docker Containers**

 ```bash
  DATABASE_HOST=localhost
  DATABASE_PORT=5432
  DATABASE_NAME=warehouse
  DATABASE_USER=user
  DATABASE_PASSWORD=secret
  AWS_ACCESS_KEY_ID=your-access-key-id
  AWS_SECRET_ACCESS_KEY=your-secret-access-key
  AWS_REGION=us-east-1
  S3_BUCKET=your-bucket-name
  ```
Ensure you have Docker and Docker Compose installed on your system. You can download and install Docker from Docker's official website.
```bash 
docker-compose up --build
```

### 3. **Start the FastAPI Application**

```bash 
uvicorn main:app --reload
```
You can interact with your FastAPI application through Swagger UI, which is available at:
http://localhost:8000/docs
### **4.Testing**
To ensure that your application works as expected, run the unit tests:
```bash 
pytest
```

### **AWS Integration**
### LocalStack
- LocalStack is used to simulate AWS services locally. The following AWS services are simulated:

-S3: Object storage service.
-SQS: Managed message queue service.
-DynamoDB: NoSQL database service.
### Initialization Scripts
- The project includes initialization scripts for setting up LocalStack resources:
- init-sqs.sh: Creates an SQS queue.
- init-s3.py: Creates an S3 bucket.

### Shipping Integration
Simulated shipping costs calculation is provided within the API.(use shippo sdk for python) 



## Note 
 - AWS Integration:
   - Keep API call tracking in DynamoDB.
   - Use S3 for image storage.
   - Leverage SQS or EventBridge for asynchronous processing of events (e.g.,low-stock notifications). : 
     - I set send_message low stock in file s3_sqs.py , and use cronjob , set 1s to send with item investory < 50
  - Integrate with a third-party shipping service (e.g., Shippo) to calculate shipping costs: 
     - shippingcost.py Here I simulate an order and get the default shipping cost each time I create an order 
  - file readDynamodb.py to read table dynamo
  - I have added 10 products and 4 default categories


## Unfamiliar Areas 
  - Identify the gaps in your knowledge by reviewing documentation and examples.: 
    - Review Documentation: Start by reading the official documentation related to the technology or concept. For FastAPI and       AWS, this would mean looking at the FastAPI documentation and AWS documentation.

  - Practice hands-on with small projects or experiments.
    - Build Small Projects: Create small, manageable projects or components related to the technology. 
    - Tutorials and Courses: Websites like Udemy, Coursera, or Codecademy offer courses on AWS, FastAPI, and related    
       technologies.
    
  - Seek help from communities or mentors when needed
    - Join Forums and Communities: Participate in relevant forums or communities. Stack Overflow, Reddit, and specific 
      technology forums can be helpful.
    - Seek Mentorship: Reach out to colleagues or mentors who have experience with the technology for guidance.






