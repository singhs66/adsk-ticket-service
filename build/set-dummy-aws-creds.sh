#!/bin/bash
# Set AWS credentials for Terraform validation/testing
cd "$(dirname "$0")/.." || exit 1
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-dummyaccesskey}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-dummysecretkey}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-west-2}"
echo "AWS credentials set for this shell session (from environment or defaults)."
