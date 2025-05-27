#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
# Update ECS service to use the latest image
echo "Updating ECS service..."
aws ecs update-service --cluster fastapi-cluster --service fastapi-service --force-new-deployment
