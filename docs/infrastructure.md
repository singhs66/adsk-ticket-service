# Infrastructure & Deployment (AWS)

## Prerequisites
- Install Terraform and AWS CLI (see [localdev.md](./localdev.md) for details).

## Infrastructure as Code (Terraform)

This project provides Terraform scripts to provision AWS resources for running the FastAPI app in production.

### AWS Resources Provisioned
- VPC, Subnet, and Internet Gateway
- Security Groups for DB and ECS
- RDS PostgreSQL database
- ECR repository for Docker images
- ECS Fargate cluster, task, and service
- IAM roles for ECS
- ElastiCache Redis cluster

### Setup Steps

1. **Set Database Credentials**
   - Edit `infrastructure/variables.tf` or use a `terraform.tfvars` file to provide `db_username` and `db_password`.

2. **Initialize Terraform**
   ```bash
   bash build/terraform-init.sh
   ```

3. **Plan Infrastructure Changes**
   ```bash
   bash build/terraform-plan.sh
   ```

4. **Apply Infrastructure Changes**
   ```bash
   bash build/terraform-apply.sh
   ```

5. **Build and Push Docker Image to ECR**
   ```bash
   bash build/build.sh
   ```

6. **Deploy to ECS**
   ```bash
   bash build/deploy.sh
   ```

---

For more, see [docker.md](./docker.md) and [secrets.md](./secrets.md).
