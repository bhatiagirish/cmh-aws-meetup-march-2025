#
# gbChatBot.py
# Version 1.0
# Created on Thu Feb 06 2025
# Created By Girish Bhatia
# Copyright (c) 2025
#



import boto3
import json
import logging
import os
from typing import Optional, Any, Dict


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Loading function")

# create a bedrock runtime client
client_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Constants for repeated strings
ACCEPT_HEADER = "application/json"
CONTENT_TYPE_HEADER = "application/json"


# get values for environment variables
# throw exception if environment variables are not set
def get_env_var(var_name: str, raise_exception: bool = True) -> Optional[str]:
    value = os.environ.get(var_name)
    if value is None and raise_exception:
        raise Exception(f"{var_name} is not set")
    return value


def get_env_var_int(var_name: str, raise_exception: bool = True) -> Optional[int]:
    value = get_env_var(var_name, raise_exception)
    if value is not None:
        try:
            return int(value)
        except ValueError:
            if raise_exception:
                raise Exception(f"{var_name} is not a valid integer")
    return None


def get_env_var_float(var_name: str, raise_exception: bool = True) -> Optional[float]:
    value = get_env_var(var_name, raise_exception)
    if value is not None:
        try:
            return float(value)
        except ValueError:
            if raise_exception:
                raise Exception(f"{var_name} is not a valid float")
    return None


# Fetch environment variables
modelId = get_env_var("modelId")
temperature = get_env_var_int("temperature")
maxTokenCount = get_env_var_int("maxTokenCount")
topP = get_env_var_float("topP")


# function to generate response using invoke API
# pass the parameters to the function
# prompt, systemPrompt
def generateConversation(prompt: str) -> Dict[str, Any]:
    logger.info("*** inside generateConversation ***")
    logger.info(f"Prompt received: {prompt}")

    # Create a prompt body for Bedrock API
    prompt_data = {
        "max_gen_len": maxTokenCount,
        "temperature": temperature,
        "top_p": topP,
        "prompt": prompt,
    }
    prompt_body = json.dumps(prompt_data)
    logger.debug(f"Prompt body: {prompt_body}")

    logger.info("*** Prior to invoking Bedrock ***")

    try:
        response = client_runtime.invoke_model(
            modelId=modelId,
            body=prompt_body,
            accept=ACCEPT_HEADER,
            contentType=CONTENT_TYPE_HEADER,
        )
        logger.info("Model invoked successfully")
    except client_runtime.exceptions.ClientError as e:
        logger.error(f"Client error invoking Bedrock model: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error invoking Bedrock model: {str(e)}")
        raise Exception(f"Failed to generate response: {str(e)}")

    return response


# Lambda function to invoke bedrock
def lambda_handler(event, context):
    prompt = ""
    if event is None:
        logger.info("Event is None")
    logger.info(f" event is --> {event}")

    # extract txt file from the event based on post method
    if event.get("httpMethod") == "POST":
        logger.info("httpMethod is POST")
        prompt = event.get("body")
        logger.info(f"prompt is *** --> {prompt}")
    else:
        logger.info("httpMethod is not POST")
        return buildResponse(400, "Only POST method is supported")
    if prompt is None:
        logger.info("prompt is None")
        return buildResponse(
            400, "No prompt found. A prompt must be provided to process the request"
        )
    response = generateConversation(prompt)
    logger.info("*** after invoking Bedrock API ***")
    # Parse and print the response
    response["body"] = json.loads(response["body"].read().decode("utf-8"))
    # extract generation from the response
    logger.info("Extracting generation from the response")
    response = response["body"]["generation"]
    logger.info(f"response is --> {response}")
    if response is None:
        return buildResponse(400, "No response found")
    return buildResponse(200, response)


# function to build responde based on status code and message
def buildResponse(statusCode, message):
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps(message, indent=4, sort_keys=True, default=str),
    }
