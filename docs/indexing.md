# Database Indexing in Ticketing System

## Overview

To ensure fast and efficient queries, especially as your ticket data grows, this project uses **database indexing** on key columns in the PostgreSQL database. Indexes help the database quickly locate and retrieve rows, improving the performance of read-heavy operations such as listing, searching, and filtering tickets.

## Indexes Used

The following indexes are created automatically when the database is initialized:

- **Status Index:**  
  Speeds up queries filtering tickets by their status (e.g., Open, Closed).
  ```
  CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
  ```

- **Created At Index:**  
  Optimizes sorting and filtering tickets by creation date, especially for recent tickets.
  ```
  CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at DESC);
  ```

- **Reporter Index:**  
  Allows fast lookups by the ticket reporter (if applicable).
  ```
  CREATE INDEX IF NOT EXISTS idx_tickets_reporter ON tickets(id);
  ```

- **Assignee Index:**  
  Improves performance when filtering or searching tickets by assignee.
  ```
  CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee);
  ```

## How Indexes Are Created

Indexes are created in the `create_indexes()` function in the database initialization code. This function runs automatically when the application starts, ensuring indexes are present even after migrations or new deployments.

## Benefits

- **Faster Queries:**  
  Indexes significantly reduce the time required for SELECT queries on indexed columns.
- **Scalability:**  
  As the number of tickets grows, indexed queries remain performant.
- **Efficient Filtering & Sorting:**  
  Users experience quick responses when filtering by status, assignee, or date.

## When to Add More Indexes

If you notice slow queries on other columns, consider adding additional indexes. However, keep in mind that too many indexes can slow down write operations (INSERT/UPDATE/DELETE).

---

**Tip:**  
You can inspect and analyze indexes in PostgreSQL using tools like `psql`, `pgAdmin`, or by running:
```sql
\d tickets
```
to see all indexes on the `tickets` table.
