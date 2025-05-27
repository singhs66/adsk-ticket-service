# Docker Build and ECS Deployment

## Build and Push Docker Image (ECR)

Before deploying to AWS ECS, you must build your Docker image and push it to the AWS ECR repository provisioned by Terraform.

### Steps:
1. **Authenticate Docker to ECR**
2. **Build the Docker image**
3. **Tag the image for ECR**
4. **Push the image to ECR**

You can use the provided script:

```bash
bash build/build.sh
```

This script will:
- Authenticate Docker to your ECR registry
- Build the Docker image using the `Dockerfile` in the project root
- Tag the image as `latest` for your ECR repo
- Push the image to ECR

**Note:** The ECR URL is hardcoded in `build/build.sh`. If your ECR repo URL is different, update the script accordingly.

---

## Deploying the Latest Image to ECS

After pushing your Docker image to ECR, you must update your ECS service to use the new image. Use the provided script:

```bash
bash build/deploy.sh
```

This script will force a new deployment of your ECS service, ensuring the latest image is pulled and new tasks are started.

---

## Deployment Steps (Summary)

1. **Plan Infrastructure Changes**
   ```bash
   bash build/terraform-plan.sh
   ```
2. **Apply Infrastructure Changes**
   ```bash
   bash build/terraform-apply.sh
   ```
3. **Build and Push Docker Image**
   ```bash
   bash build/build.sh
   ```
4. **Deploy to ECS**
   ```bash
   bash build/deploy.sh
   ```

For AWS secrets and environment setup, see [secrets.md](./secrets.md).
