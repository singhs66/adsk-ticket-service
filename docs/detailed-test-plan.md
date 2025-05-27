#  Test Plan – Autodesk Tickets Project

A comprehensive test plan to ensure the correctness, security, and reliability of the FastAPI-based ticketing system. 

---

## Overview

This system enables users to register, authenticate, and manage support tickets via a web UI and RESTful API, with Slack notifications integrated for real-time team visibility.

---

## Objectives

- Ensure all core API functionality (register, token, create/read/update/delete tickets) works as expected.
- Validate JWT-based authentication and route protection.
- Confirm data is correctly persisted and updated in PostgreSQL.
- Test Slack notifications are triggered appropriately.
- Test Redis caching and cache invalidation (see [redis.md](./redis.md)).

---

## Scope

### In Scope

- `/register`, `/token`, `/tickets/`, `/tickets/{id}` API endpoints
- Authentication & authorization workflows
- PostgreSQL database interactions
- Redis caching and invalidation
- Slack notification logic

### Out of Scope

- UI/Frontend behavior
- Non-Slack third-party integrations

---

##  Test Environment

| Component       | Stack                                  |
|----------------|-----------------------------------------|
| Backend         | FastAPI + Python                       |
| Auth            | JWT (PyJWT)                            |
| Database        | PostgreSQL                             |
| Caching         | Redis (ElastiCache or local)           |
| Slack           | Incoming Webhooks                      |
| Testing Tools   | `pytest`, `TestClient`, `unittest.mock` |

---

##  Test Types

- **Unit Tests**: Validate isolated functions (e.g., password hashing, token creation)

---

## Test Cases

###  User Registration

- **Success** – Register with valid data → 200 OK
- **Conflict** – Register with existing email → 409 Conflict

### Authentication

- **️ Login Success** – Correct credentials → 200 OK + JWT
- **Login Fail** – Wrong password → 400 Bad Request

### Ticket Management

- **Create Ticket** – Valid input → 200 OK
- **Read Ticket** – Existing ID → returns ticket
- **Read Invalid ID** – Nonexistent → 404 Not Found
- **Update Ticket** – Valid PUT → updated ticket
- **Delete Ticket** – Valid ID → 200 OK + confirmation

###  Slack Integration

- **On Create** – New ticket sends Slack message
- **On Update** – Status/description change sends Slack message
- **Slack Fail** – Slack webhook down → logs error (but API succeeds)

---

## Test Execution

Run these tests locally

---

## Acceptance Criteria

- 100% pass rate for all core APIs
- Proper token validation and protected access
- Slack messages fire reliably for all ticket state changes
- No regressions across API versions

---

For Redis-specific tests, see [redis.md](./redis.md).

