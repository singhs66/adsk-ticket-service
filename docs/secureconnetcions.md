## HTTPS Request Flow Diagram (with AWS ACM, ALB, and ECS)

Below is a high-level flow diagram showing how an HTTPS request is handled from the client to the backend service running on ECS:

```
[Client Browser]
      |
      |  (HTTPS Request: https://tickets.example.com)
      v
[AWS Application Load Balancer (ALB)]
      |
      |---> [ALB uses ACM Certificate to terminate SSL/TLS]
      |         (Certificate is validated; secure connection established)
      |
      |  (ALB forwards decrypted HTTP request)
      v
[Target Group (ECS Service)]
      |
      v
[ECS Fargate Task / Container (FastAPI App)]
      |
      v
[Response flows back through ALB to Client over HTTPS]
```

**Steps:**
1. **Client** sends an HTTPS request to your domain.
2. **ALB** receives the request and uses the ACM-provided SSL/TLS certificate to decrypt and validate the connection.
3. **ALB** forwards the now-unencrypted HTTP request to the ECS service (within a private or public subnet).
4. **ECS** container processes the request and sends the response back to the ALB.
5. **ALB** re-encrypts the response (if needed) and sends it back to the client over HTTPS.

This setup ensures secure communication between the client and AWS, while allowing efficient routing and scaling of backend services.