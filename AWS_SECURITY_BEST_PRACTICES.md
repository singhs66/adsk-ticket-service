# AWS Security Best Practices for FastAPI ECS Infrastructure

This document outlines the key AWS security best practices implemented (and recommended) for your FastAPI deployment on ECS Fargate, ALB, and RDS using Terraform.

---

## 1. Restrict Security Group Ingress Rules
- **ECS Task Security Group:**
  - Only allows inbound traffic on port 8000 from the ALB security group (not from all sources).
- **ALB Security Group:**
  - Only allows inbound traffic on port 8000 from trusted IP ranges (not from `0.0.0.0/0`).
- **RDS Security Group:**
  - Should only allow inbound traffic from the ECS security group (not from `0.0.0.0/0`).

## 2. Use HTTPS for ALB
- Add an HTTPS listener to your ALB.
- Attach an AWS ACM SSL certificate.
- Redirect HTTP to HTTPS for all traffic.

## 3. Store Secrets Securely with AWS Secrets Manager
- **Implemented:**
  - Created a secret in AWS Secrets Manager for the database password (`fastapi/production/db_password`).
  - Referenced the secret in the ECS task definition using the `secrets` block, so the value is injected as the `DB_PASSWORD` environment variable.
  - Updated the ECS task execution role to allow `secretsmanager:GetSecretValue` for the secret.
- **Terraform Resources:**
  - `aws_secretsmanager_secret` and `aws_secretsmanager_secret_version` for secret management.
  - `aws_iam_policy` and `aws_iam_role_policy_attachment` for IAM permissions.
- **Best Practice:**
  - No sensitive values are hardcoded in code or Dockerfile. All secrets are managed via AWS Secrets Manager and injected securely at runtime.

## 4. Limit IAM Permissions
- ECS task execution role only has permissions for ECR, CloudWatch Logs, and Secrets Manager (if used).
- Avoid using overly broad IAM policies.

## 5. Enable Logging and Monitoring
- **CloudWatch Logs:** ECS task logs are sent to a dedicated log group (`/ecs/fastapi`).
- **ALB Access Logs:** Enable and send to an S3 bucket for auditability.

## 6. Use Private Subnets for ECS Tasks
- Place ECS tasks in private subnets (with NAT Gateway for outbound internet access), not public subnets, unless public access is required.
- Only the ALB should be in a public subnet.

## 7. Database Security
- Restrict RDS/Postgres security group to only allow inbound traffic from the ECS security group.
- Enable encryption at rest and in transit for RDS.

## 8. Set Resource Limits
- Set appropriate CPU and memory limits for ECS tasks to prevent resource exhaustion.

## 9. Keep Images and Dependencies Updated
- Regularly update your Docker base images and Python dependencies to patch vulnerabilities.

## 10. Use Environment Variables for Configuration
- Do not hardcode sensitive values in your code or Dockerfile.

## 11. Enable Container Insights (Optional)
- For deeper monitoring, enable ECS Container Insights in CloudWatch.

## 12. Restrict Outbound Traffic (Optional)
- Use VPC security group egress rules to restrict outbound traffic from ECS tasks if possible.

---

## Additional Recommendations
- Rotate secrets and credentials regularly.
- Use AWS Config and GuardDuty for continuous security monitoring.
- Enable multi-factor authentication (MFA) for all AWS IAM users.
- Regularly review IAM users, roles, and policies.

---

**Review and implement these best practices to keep your AWS infrastructure secure and compliant.**
