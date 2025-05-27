#!/bin/bash
# Build and push Docker image to ECR
ECR_URL="600946769731.dkr.ecr.us-west-2.amazonaws.com/fastapi-app"

# Always run from the project root (tickets directory)
cd "$(dirname "$0")/.."

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin "$ECR_URL"
docker build --platform linux/amd64 -t fastapi-app -f Dockerfile .
docker tag fastapi-app:latest "$ECR_URL":latest
docker push "$ECR_URL":latest
