######################################################################
# Script to manage the bot, the API can triggered by slack via auth #
# this script will be running by API Gateway                        #
# Add api gateway, then add Integration Request > mapping template  #
# Content Type: application/x-www-form-urlencoded                   #
# Put this body: {"body": $input.json("$")}                         #
# author: wansatriaandanu@gmail.com                                 #
######################################################################

import boto3
import json
import logging
import os
import datetime

from base64 import b64decode
from urlparse import parse_qs
from botocore.vendored import requests

lambda_client = boto3.client("lambda", region_name="ap-southeast-1")


# ENCRYPTED_EXPECTED_TOKEN = os.environ['EncryptedToken']
#
# # NOT USING THIS, CAUSE HAVE SOME PROBLEM WITH PERMISSION IAM KMS
# #kms = boto3.client('kms')
# #expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']
# expected_token = ENCRYPTED_EXPECTED_TOKEN

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    command_text = params['text'][0]

    # slack webhook
    slack_webhook_url = '<wehbook url>'

    if command_text == "command_restore_database_a": # you can define which command are valid or not
    # Then inside this you can call another worker function
        slack_data = {
            "attachments": [
                {
                    "title": "Hi "+ user + ", thanks for calling, i'm ready to served you :smile: ",
                    "color": "#36a64f",
                    "mrkdwn_in": [
                        "text",
                        "pretext"
                    ]
                }
            ]
        }

        response_slack = requests.post(
          slack_webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
        )
        payload = {"parameter": command_text}
        resp = lambda_client.invoke(FunctionName="sre-bot-dbsimulation", InvocationType='RequestResponse', Payload = json.dumps(payload))

        return respond(None, "Success")
    elif command_text  == "command_restore_database_b":
        slack_data = {
            "attachments": [
                {
                    "title": "Hi "+ user + ", thanks for calling, i'm ready to served you :smile: ",
                    "color": "#36a64f",
                    "mrkdwn_in": [
                        "text",
                        "pretext"
                    ]
                }
            ]
        }

        response_slack = requests.post(
          slack_webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
        )

        payload = {"parameter": command_text}
        resp = lambda_client.invoke(FunctionName="sre-bot-dbsimulation", InvocationType='RequestResponse', Payload = json.dumps(payload))

        return respond(None, "Success")
    else:
        return respond(None, "Invalid Command")
