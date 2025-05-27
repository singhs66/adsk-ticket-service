# Secrets Management

This project uses AWS Systems Manager (SSM) Parameter Store and ECS secrets to securely store sensitive values, such as the database password and Redis URL.

## How it works
- The database password is stored in AWS SSM Parameter Store under a parameter name (e.g., `/fastapi/production/db_password`).
- The Redis URL is set as an environment variable or ECS secret.
- The FastAPI app retrieves secrets at startup using the AWS SDK (`boto3`) or from environment variables.
- The ECS task execution role (or your local AWS credentials) must have permission to read the parameter from SSM.

## How to set/update the secret
1. Set or update the parameter in AWS SSM Parameter Store:
   ```bash
   aws ssm put-parameter --name "/fastapi/production/db_password" --value "YOUR_PASSWORD" --type "SecureString" --overwrite
   ```
2. Ensure your ECS task role or local AWS credentials have `ssm:GetParameter` permission for this parameter.
3. Set the Redis URL in your ECS task definition or `.env` file:
   ```env
   REDIS_URL=redis://<your-elasticache-endpoint>:6379/0
   ```

## Reference in your application
- The FastAPI app reads the parameter name from the `DB_PASSWORD_PARAM_NAME` environment variable.
- At startup, the app fetches the password from SSM using `boto3` and uses it to construct the database connection string.
- See `app/daoLayer/database.py` for implementation details.

For local development, see [localdev.md](./localdev.md).
