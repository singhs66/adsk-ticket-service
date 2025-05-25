# Create a secret for DB password (example, can be extended for other secrets)
# resource "aws_secretsmanager_secret" "fastapi_db_password" {
#   name        = "fastapi/production/db_password"
#   description = "Database password for FastAPI production environment"
# }
#
# resource "aws_secretsmanager_secret_version" "fastapi_db_password" {
#   secret_id     = aws_secretsmanager_secret.fastapi_db_password.id
#   secret_string = var.db_password
# }

resource "aws_ssm_parameter" "db_password" {
  name  = "/fastapi/production/db_password"
  type  = "SecureString"
  value = var.db_password
}
