from datetime import datetime
from unittest.mock import patch

from pydantic import UUID1

from app.integrations.slackbot.slackbot import send_slack_notification_create
from app.daoLayer.serviceObjects.TicketSO import TicketSO

ticket = TicketSO(
    id=UUID1("05901d2e-3df3-4822-b43d-0b4c5185bd84"),
    title="Login Error",
    description="Cannot log in",
    status="open",
    severity="high",
    category="UX",
    created_at=datetime.now()
)

def test_slack_notification_created(mock_post):
    mock_post.return_value.status_code = 200
    send_slack_notification_create(ticket, "Created")
    mock_post.assert_called_once()