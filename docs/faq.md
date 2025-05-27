# FAQ

**Why did we choose JWT over OAuth2?**

We use JWT (JSON Web Tokens) as the token format for authentication because it is lightweight, stateless, and easy to implement for API authentication in microservices. 
While OAuth2 is an authorization framework that can use JWT as a token format, full OAuth2 implementations are more complex and often require additional infrastructure (like an authorization server) and are best suited for scenarios involving third-party access delegation.

For this project:
- We only need simple, secure user authentication and route protection, not third-party authorization.
- JWT allows us to encode user identity and claims directly in the token, which can be validated without a database lookup.
- FastAPI provides built-in support for JWT-based authentication, making integration straightforward.

**Why did you choose ECS Fargate and ALB over other options like EC2 or API Gateway?**

Fargate abstracts away server management while still giving me control over container networking and IAM. 
It’s ideal for managing isolated microservices like a ticketing API. I chose ALB because I needed path-based routing, SSL termination (via ACM), and session stickiness — which API Gateway didn’t provide as easily without additional Lambda proxies.

**How would you handle high write volume or concurrent updates to a ticket?**

For concurrency, PostgreSQL handles ACID compliance and row-level locking. In the app, each update uses a consistent DB session and commits are followed by db.refresh() to get the latest state. 
If this scaled further, I’d consider optimistic locking using a version field or timestamp, and implement conflict resolution for concurrent writes.

In summary, JWT is used for its simplicity and efficiency, while OAuth2 is more suitable for advanced authorization scenarios.

**Q: Are you running the service in public or private subnet  ?**
- **Current Architecture:**  
  For the scope of this project, all AWS resources (ECS tasks, RDS, ElastiCache, etc.) are deployed in a public subnet to simplify access and testing.

- **Future Vision:**  
  The long-term plan is to migrate all compute and data resources (ECS, RDS, ElastiCache) into private subnets for enhanced security. Only the Application Load Balancer (ALB) will remain in the public subnet to handle external traffic and securely route requests to internal resources.

**Q: How did you decide your key and value for your redis cache ?**

For individual tickets, the cache key is set as `ticket:{id}`, where `{id}` is the unique ticket identifier. This ensures fast and direct access to a specific ticket.

For ticket list queries, the cache key is constructed as `tickets:all:{status}:{sort_by}:{assignee}`. This pattern uniquely identifies a set of tickets based on the applied filters and sorting, allowing efficient caching and retrieval of filtered ticket lists.

In both cases, the value stored is the serialized ticket object or list (typically as JSON). This approach supports quick lookups, easy cache invalidation when tickets change, and aligns with best practices for caching both single objects and query results.

**Q: How did you prevent SQL injections ?**

The ticketing system prevents SQL injection attacks through the following measures:

- **ORM Usage:**  
  All database operations use SQLAlchemy ORM, which automatically parameterizes queries. This ensures that user input is never directly interpolated into raw SQL statements.

- **No Raw SQL from User Input:**  
  The application does not construct SQL queries by concatenating or interpolating user-provided data. All filters and lookups (e.g., by status, assignee, ticket ID) are performed using SQLAlchemy's query methods, which safely handle parameters.

- **Input Validation:**  
  Pydantic models are used to validate and sanitize incoming request data before it reaches the database layer.

- **Parameterized Queries:**  
  Even in cases where raw SQL might be used (such as for index creation), parameters are never directly inserted from user input.

**Q: How did you prevent XSS injections ?**

- **Input Validation:**  
  All incoming data is validated and sanitized using Pydantic models, ensuring that only expected data types and formats are accepted.

- **Output Encoding:**  
  The frontend (e.g., React) is responsible for properly encoding and escaping any user-generated content before rendering it in the browser, preventing malicious scripts from executing.

- **No Direct HTML Rendering:**  
  The backend API does not return raw HTML or render templates with user input, reducing the risk of reflected or stored XSS.

**Q: Why did we use Relational Database ?**
- PostgreSQL was selected for this project due to its strong support for structured, relational data and transactional consistency.
- Tickets inherently have relationships (e.g., users, assignees, statuses), and the need for features like filtering, sorting, pagination, and constraints (e.g., unique ticket IDs, length limits) made a relational database a natural fit.

**Q: How is the system highly available ?**
- The service is deployed in multi AZ's ensuring high availability  

**Q: How is the system highly scale ?**
- The service is deployed behind a load balancer and on AWS ECS which ensures our system would scale under high load.

**Q: Will Terraform automatically store state files when I run `terraform apply` for the first time? Where are they stored?**
- By default, Terraform stores state files locally in the `infrastructure/` directory as `terraform.tfstate`.
- If you want to store state remotely (e.g., in S3 for team use and safety), you must configure a backend in your Terraform files. This project currently uses local state by default.

**Q: How do I test Redis caching on AWS?**
- See [redis.md](./redis.md) for step-by-step Redis testing and troubleshooting.

**Q: Where do I set secrets for the app?**
- See [secrets.md](./secrets.md) for AWS SSM and ECS secrets setup.

**Q: How do I run the app locally?**
- See [localdev.md](./localdev.md) for local setup instructions.
