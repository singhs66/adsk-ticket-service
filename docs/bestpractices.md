# Improvements & Best Practices

- Use remote state (S3) for Terraform in production.
- Restrict security group ingress rules for better security.
- Use AWS Secrets Manager or SSM Parameter Store for DB credentials and secrets in production.
- Add CI/CD for automated deploys.
- Use environment variables for configuration.
- Monitor ECS, RDS, and ElastiCache with CloudWatch.
- Regularly update dependencies and base images.
- Use JWT for all protected endpoints.
- Reference [architecture.md](./architecture.md) and [infrastructure.md](./infrastructure.md) for more.
