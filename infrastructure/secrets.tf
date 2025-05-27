resource "aws_ssm_parameter" "db_password" {
  name  = "/fastapi/production/db_password"
  type  = "SecureString"
  value = var.db_password
}

resource "aws_ssm_parameter" "slack_webhook_url" {
  name  = "/fastapi/production/slack_webhook_url"
  type  = "SecureString"
  value = var.slack_webhook_url
}
