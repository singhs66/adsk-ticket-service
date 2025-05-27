from fastapi.testclient import TestClient
from main import app  # Adjust based on your FastAPI entrypoint
from app.auth.jwt import create_access_token

client = TestClient(app)

# Create a sample JWT token
def get_auth_headers():
    token = create_access_token({"sub": "testuser@example.com"})
    return {"Authorization": f"Bearer {token}"}

def test_create_ticket():
    response = client.post(
        "/tickets/",
        json={
            "title":"Test Ticket",
                        "description":"This is a test ticket",
                        "severity":"low",
                        "category":"UX"
        },
        headers=get_auth_headers()
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ticket"

def test_list_tickets():
    response = client.get("/tickets/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_ticket():
    # Create a ticket first
    create_res = client.post(
        "/tickets/",
        json={"title":"Test Ticket",
                        "description":"This is a test ticket",
                        "severity":"low",
                        "category":"UX"},
        headers=get_auth_headers()
    )
    assert create_res.status_code == 200
    ticket_id = create_res.json()["id"]
    print("Created:", ticket_id)

    # Fetch the ticket
    get_res = client.get(f"/tickets/{ticket_id}", headers=get_auth_headers())
    assert get_res.status_code == 200, f"Get failed: {get_res.json()}"
    assert get_res.json()["id"] == ticket_id

def test_update_ticket():
    res = client.post(
        "/tickets/",
        json={"title":"Test Ticket",
                        "description":"This is a test ticket",
                        "severity":"low",
                        "category":"UX"},
        headers=get_auth_headers()
    )
    ticket_id = res.json()["id"]

    update = client.put(
        f"/tickets/{ticket_id}",
        json={"description": "updated", "status": "in_progress"},
        headers=get_auth_headers()
    )
    assert update.status_code == 200
    assert update.json()["status"] == "in_progress"


def test_delete_ticket():
    res = client.post(
        "/tickets/",
        json={"title":"Test Ticket",
                        "description":"This is a test ticket",
                        "severity":"low",
                        "category":"UX"},
        headers=get_auth_headers()
    )
    ticket_id = res.json()["id"]

    delete = client.delete(f"/tickets/{ticket_id}", headers=get_auth_headers())
    assert delete.status_code == 200
    assert delete.json()["message"] == "Ticket deleted"



