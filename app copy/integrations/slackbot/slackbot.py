import requests

from app.daoLayer.serviceObjects import TicketSO

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
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
