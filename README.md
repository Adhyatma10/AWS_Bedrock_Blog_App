# AWS_Bedrock_Blog_App
Blog generation app using AWS Bedrock.


# **Blog Generation System with AWS Bedrock, API Gateway, Lambda, and Pinecone**

This project is a serverless application that generates a blog based on a user-defined topic using AWS Bedrock’s foundation models. The generated blog is stored in an Amazon S3 bucket, and the system communicates through an API Gateway. Pinecone is used to trigger the API, while the Lambda function is enhanced with a custom layer containing the latest boto3 library to handle AWS services effectively.

## **Table of Contents**
- [Introduction](#introduction)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [AWS IAM Role Configuration](#aws-iam-role-configuration)
  - [S3 Bucket Setup](#s3-bucket-setup)
  - [Lambda Function Deployment](#lambda-function-deployment)
  - [API Gateway Setup](#api-gateway-setup)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)

## **Introduction**
This project implements a serverless solution to generate and store blogs based on a provided topic. The solution integrates AWS services like Bedrock for AI-powered blog generation, S3 for storage, API Gateway for handling requests, and Pinecone for triggering the blog generation API. The Lambda function also leverages a custom layer with the latest boto3 library for effective service communication.

## **Architecture**

The overall architecture includes the following:
1. **API Gateway**: Serves as the entry point to trigger the blog generation request.
2. **AWS Bedrock**: A foundation model from AWS Bedrock is invoked to generate a blog on a user-provided topic.
3. **AWS Lambda**: Handles the logic for generating and storing the blog, using the latest boto3 library via a custom Lambda layer.
4. **Amazon S3**: Stores the generated blog as a `.txt` file in a predefined S3 bucket.
5. **Pinecone**: Used to trigger the API Gateway endpoint, initiating the blog generation.

### Architecture Flow:
1. The API Gateway receives a request with the blog topic.
2. The Lambda function processes the request, sends the topic to AWS Bedrock’s foundation model for blog generation, and receives the result.
3. The generated blog is saved to an S3 bucket with a timestamp-based filename.
4. Pinecone triggers the entire flow by calling the API Gateway.

## **Technologies Used**
- **AWS API Gateway**: For receiving requests and triggering the Lambda function.
- **AWS Lambda**: Serverless compute function that handles blog generation and S3 storage.
- **AWS Bedrock**: To generate a blog using a foundation model.
- **Amazon S3**: For storing the generated blog files.
- **Pinecone**: To trigger the API request.
- **Python 3.9+**: Lambda function runtime.

## **Setup Instructions**

### Prerequisites
1. **AWS Account**: Required to access Bedrock, Lambda, API Gateway, S3, and IAM.
2. **Pinecone Account**: To configure Pinecone for API triggering.
3. **Python 3.9+**: For local development and testing.

### AWS IAM Role Configuration
1. **Lambda Execution Role**:
   - Create an IAM role for the Lambda function with the following permissions:
     - `AmazonS3FullAccess` for storing the blog.
     - `BedrockInvokeModelPolicy` for accessing the Bedrock foundation model.
     - `APIGatewayInvokeFullAccess` for handling API Gateway requests.
   - Attach the role to the Lambda function.

### S3 Bucket Setup
1. Create an S3 bucket to store the generated blog files.
2. Ensure the Lambda function has `s3:PutObject` permission for the bucket.

### Lambda Function Deployment
1. Create the Lambda function in AWS Lambda console.
2. Upload the function code and create a custom Lambda layer with the latest `boto3`/`botocore` libraries.
3. Set environment variables for the S3 bucket name and other configurable parameters.

### API Gateway Setup
1. Create an API Gateway endpoint that triggers the Lambda function.
2. Configure the API to accept POST requests with a JSON payload (blog topic).
3. Link the API Gateway to the Lambda function.

## **How It Works**

1. **Input**: The system is triggered by Pinecone or a direct request to API Gateway with the blog topic.
2. **Blog Generation**: The blog topic is sent to the AWS Bedrock model for generation using the `llama3-8b-instruct-v1:0` foundation model.
3. **Storage**: The generated blog is saved to S3 with a unique filename based on the timestamp.
4. **Response**: The system returns a response indicating that the blog generation and storage process has been completed.

## **Usage**
- Trigger the API Gateway with a JSON request that contains the blog topic:
  ```json
  {
    "blog_topic": "The impact of AI on healthcare"
  }
  ```
- Pinecone can be configured to trigger this API programmatically or via user input.

## *Flowchart*
<img width="534" alt="image" src="https://github.com/user-attachments/assets/20eb0fd1-33eb-443a-8b54-de2d0e0d3b34">

