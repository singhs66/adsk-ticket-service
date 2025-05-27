import requests
import os
import boto3

from app.daoLayer.serviceObjects import TicketSO

# Retrieve Slack webhook URL from SSM Parameter Store if not set in env
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "us-west-2"))
    param = ssm.get_parameter(Name="/fastapi/production/slack_webhook_url", WithDecryption=True)
    SLACK_WEBHOOK_URL = param["Parameter"]["Value"]


print(f"Using Slack webhook URL: {SLACK_WEBHOOK_URL}")

def send_slack_notification_create(ticketSO: TicketSO, action: str):
    if action == "Created":
        message = {
            "text": f":new: *New Ticket Created!*\n*Title:* {ticketSO.title}\n*Severity:* {ticketSO.status}\n*Description:* {ticketSO.description}"
        }
    else:
        message = {
            "text": f":up: *Existing Ticket Updated!*\n*Title:* {ticketSO.title}\n*Severity:* {ticketSO.status}\n*Description:* {ticketSO.description}"
        }

    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print(f"Slack notification failed: {response.text}")
