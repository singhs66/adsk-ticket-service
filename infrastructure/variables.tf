variable "aws_region" {
  description = "AWS region to deploy resources in."
  default     = "us-west-2"
}

variable "db_username" {
  description = "Database master username."
  type        = string
  default     = "ticket"
}

variable "db_password" {
  description = "Database master password. (stored in Secrets Manager)"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Database name."
  default     = "ticket-service"
}

variable "alb_domain_name" {
  description = "The domain name for the ALB ACM certificate."
  type        = string
}

variable "route53_zone_id" {
  description = "The Route53 Hosted Zone ID for ACM DNS validation."
  type        = string
}

variable "db_password_param_name" {
  description = "Name of the SSM parameter for the database password."
  type        = string
  default     = "/fastapi/production/db_password"
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications. (stored in SSM Parameter Store)"
  type        = string
  sensitive   = true
}
