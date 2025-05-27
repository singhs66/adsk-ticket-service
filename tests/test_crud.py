import pytest
import json
from unittest.mock import patch, MagicMock
from uuid import uuid4

from app.apiSchemas import TicketCreate
import app.crud as crud

@pytest.fixture
def ticket_create_data():
    return TicketCreate(
        title="Test Ticket",
        description="A test ticket",
        severity="high",
        category="Bug",
        status="Open"
    )

def test_create_ticket(ticket_create_data):
    with patch("app.crud.create_ticket_dao") as mock_create_ticket_dao, \
         patch("app.crud.assign_tickets_randomly", return_value="Alice Johnson"):
        ticket = crud.create_ticket(ticket_create_data)
        assert ticket.title == "Test Ticket"
        assert ticket.assignee == "Alice Johnson"
        mock_create_ticket_dao.assert_called_once()

def test_serialize_ticket_with_model_dump():
    class Dummy:
        def model_dump(self):
            return {"id": "1", "title": "Test"}
    result = crud.serialize_ticket(Dummy())
    assert result == {"id": "1", "title": "Test"}

def test_serialize_ticket_with_dict():
    class Dummy:
        def dict(self):
            return {"id": "1", "title": "Test"}
    result = crud.serialize_ticket(Dummy())
    assert result == {"id": "1", "title": "Test"}

def test_serialize_ticket_with___dict__():
    class Dummy:
        def __init__(self):
            self.id = "1"
            self.title = "Test"
            self._sa_instance_state = "should be removed"
    result = crud.serialize_ticket(Dummy())
    assert result == {"id": "1", "title": "Test"}


def test_get_all_tickets_cache_hit():
    with patch("app.crud.RedisCache.get", return_value=json.dumps([{"id": "1"}])) as mock_get:
        result = crud.get_all_tickets("Open", "created_at", "Alice")
        assert result == [{"id": "1"}]
        mock_get.assert_called_once()

def test_get_all_tickets_cache_miss():
    with patch("app.crud.RedisCache.get", return_value=None), \
         patch("app.crud.list_ticket_dao", return_value=[MagicMock()]) as mock_list_ticket_dao, \
         patch("app.crud.RedisCache.set") as mock_set, \
         patch("app.crud.serialize_ticket", return_value={"id": "1"}):
        result = crud.get_all_tickets("Open", "created_at", "Alice")
        assert isinstance(result, list)
        mock_list_ticket_dao.assert_called_once()
        mock_set.assert_called_once()

def test_get_ticket_cache_hit():
    with patch("app.crud.RedisCache.get", return_value=json.dumps({"id": "1"})) as mock_get:
        result = crud.get_ticket("1")
        assert result == {"id": "1"}
        mock_get.assert_called_once()

def test_get_ticket_cache_miss():
    with patch("app.crud.RedisCache.get", return_value=None), \
         patch("app.crud.get_ticket_dao", return_value=MagicMock()) as mock_get_ticket_dao, \
         patch("app.crud.RedisCache.set") as mock_set, \
         patch("app.crud.serialize_ticket", return_value={"id": "1"}):
        result = crud.get_ticket("1")
        assert mock_get_ticket_dao.called
        mock_set.assert_called_once()

def test_update_ticket():
    with patch("app.crud.update_ticket_dao", return_value="updated") as mock_update, \
         patch("app.crud.RedisCache.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        result = crud.update_ticket("1", {"status": "Closed"})
        assert result == "updated"
        assert mock_client.delete.call_count == 2

def test_delete_ticket():
    with patch("app.crud.delete_ticket_dao", return_value="deleted") as mock_delete, \
         patch("app.crud.RedisCache.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        result = crud.delete_ticket("1")
        assert result == "deleted"
        assert mock_client.delete.call_count == 2

def test_assign_tickets_randomly():
    assignee = crud.assign_tickets_randomly()
    assert isinstance(assignee, str)
    assert assignee  # Should not be empty