# AWS Bedrock Lambda Chatbot API

A serverless chatbot implementation using AWS Lambda and Amazon Bedrock's DeepSeek Distilled model, deployable with AWS SAM (Serverless Application Model).

## Description

This project implements a serverless chatbot API that leverages Amazon Bedrock's DeepSeek Distilled foundation model through a Lambda function. The chatbot function is exposed as an API endpoint using Amazon API Gateway and accepts prompts via HTTP POST requests to generate AI responses.

## Features

- Serverless architecture using AWS Lambda
- API Gateway integration for HTTP endpoint exposure
- Integration with Amazon Bedrock's DeepSeek Distilled model
- Environment variable configuration for model parameters
- Error handling and logging
- CORS-enabled API endpoints

## Prerequisites

- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Python 3.9 or higher
- Access to Amazon Bedrock service
- Appropriate IAM roles and permissions
- Import DeepSeek Distilled model in Amazon Bedrock

## Environment Variables

The following environment variables must be configured:

- `modelId`: The Amazon Bedrock model identifier for DeepSeek Distilled
- `temperature`: Integer value controlling response randomness
- `maxTokenCount`: Integer value for maximum token generation
- `topP`: Float value between 0 and 1 that controls the cumulative probability threshold for token selection

## Deployment

1. Build the application using sam
```bash
sam build

Deploy the application:

sam deploy --guided

During the guided deployment, you'll need to:

Specify a stack name

Choose an AWS Region

Configure environment variables

Confirm IAM role creation

After deployment, you will receive an API Gateway endpoint URL that can be used to interact with the chatbot.

API Usage
The Lambda function is exposed through API Gateway and accepts POST requests with the following structure:

{
    "body": "Your prompt text here"
}


Successful responses will have a 200 status code and include the generated text from the DeepSeek model. Error responses will have appropriate status codes (400 for client errors) and error messages.
```

## Error Handling

The application includes error handling for:

Missing environment variables

Invalid input types

API invocation failures

Model generation errors

API Gateway integration issues

## Logging

The application uses CloudWatch Logs with INFO level logging by default, tracking:

Function invocations

API requests and responses

Error conditions

Model interaction status

API Gateway access logs

## Security

All sensitive configuration is managed through environment variables

CORS headers are configured for API security

AWS IAM roles control access to services

Input validation on all requests

API Gateway throttling and request validation

## Architecture

The solution follows a serverless architecture pattern:

Client sends request to API Gateway endpoint

API Gateway triggers Lambda function

Lambda function processes request and calls Amazon Bedrock

DeepSeek Distilled model generates response

Response is returned through API Gateway to client

## License
Copyright (c) 2025 Girish Bhatia. All rights reserved.

## Version
1.0
