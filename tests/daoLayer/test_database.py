import pytest
from unittest.mock import patch, MagicMock
from app.daoLayer.database import (
    create_ticket_dao,
    list_ticket_dao,
    get_ticket_dao,
    update_ticket_dao,
    delete_ticket_dao,
    create_indexes,
)
from app.daoLayer.serviceObjects import TicketSO
from app.apiSchemas import TicketUpdate

@pytest.fixture
def mock_db_session():
    with patch("app.daoLayer.database.SessionLocal") as mock_session:
        yield mock_session

def test_create_ticket_dao_success(mock_db_session):
    ticketSO = MagicMock(spec=TicketSO)
    db_instance = mock_db_session.return_value
    with patch("app.daoLayer.database.ticketMapper", return_value=MagicMock()), \
         patch("app.daoLayer.database.send_slack_notification_create") as mock_slack:
        result = create_ticket_dao(ticketSO)
        db_instance.add.assert_called_once()
        db_instance.commit.assert_called_once()
        db_instance.refresh.assert_called_once()
        mock_slack.assert_called_once()
        assert result is not None

def test_list_ticket_dao(mock_db_session):
    db_instance = mock_db_session.return_value
    db_instance.query.return_value.filter.return_value.filter.return_value.all.return_value = [MagicMock()]
    result = list_ticket_dao("Open", "created_at", "Alice")
    assert isinstance(result, list)

def test_get_ticket_dao(mock_db_session):
    db_instance = mock_db_session.return_value
    db_instance.query.return_value.filter.return_value.first.return_value = MagicMock()
    result = get_ticket_dao("some-id")
    assert result is not None

def test_update_ticket_dao_success(mock_db_session):
    db_instance = mock_db_session.return_value
    ticket = MagicMock()
    db_instance.query.return_value.filter.return_value.first.return_value = ticket
    update = TicketUpdate(status="Closed", description="Updated desc")
    with patch("app.daoLayer.database.send_slack_notification_create") as mock_slack:
        result = update_ticket_dao("some-id", update)
        db_instance.commit.assert_called_once()
        db_instance.refresh.assert_called_once()
        mock_slack.assert_called_once()
        assert result == ticket


def test_delete_ticket_dao_success(mock_db_session):
    db_instance = mock_db_session.return_value
    db_instance.query.return_value.filter.return_value.delete.return_value = 1
    result = delete_ticket_dao("some-id")
    db_instance.commit.assert_called_once()
    assert result is True

def test_delete_ticket_dao_not_found(mock_db_session):
    db_instance = mock_db_session.return_value
    db_instance.query.return_value.filter.return_value.delete.return_value = 0
    with pytest.raises(Exception):
        delete_ticket_dao("some-id")

def test_create_indexes(mock_db_session):
    db_instance = mock_db_session.return_value
    db_instance.execute.return_value = None
    create_indexes()
    assert db_instance.execute.call_count >= 1
    db_instance.commit.assert_called_once()