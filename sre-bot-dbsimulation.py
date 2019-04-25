import json
from botocore.vendored import requests

def lambda_handler(event, context):
    ## GET DATA PARAMETER FROM sre-bot.py
    raw_data = json.dumps(event)
    data = json.loads(raw_data)
    DBparameter = data["parameter"]
    print DBparameter

    # Slack webhook
    slack_webhook_url = 'slack_webhook_url'

    url = "https://jenkins_url/job/Restore_DB/buildWithParameters?DBName=" + DBparameter 

    print url

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    r = requests.post(url, headers=headers, auth=('username', 'jenkins_token'), data={'Submit' : 'Build'})

    print(r.status_code)

    if r.status_code != 201:
        slack_data = {
            "attachments": [
                {
                    "title": "Something went wrong to spawn simulation please report to #sre channel",
                    "color": "#A41313",
                    "mrkdwn_in": [
                        "text",
                        "pretext"
                    ]
                }
            ]
        }

        response_slack = requests.post(slack_webhook_url, data=json.dumps(slack_data),headers={'Content-Type': 'application/json'})
        if response_slack.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response_slack.status_code, response_slack.text)
            )
    else:
        slack_data = {
            "attachments": [
                {
                    "title": "Restoring latest data to "+ DBparameter + " database it will takes 15 mins. ",
                    "color": "#36a64f",
                    "mrkdwn_in": [
                        "text",
                        "pretext"
                    ]
                }
            ]
        }

        response_slack = requests.post(slack_webhook_url, data=json.dumps(slack_data),headers={'Content-Type': 'application/json'})
        if response_slack.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response_slack.status_code, response_slack.text)
            )
