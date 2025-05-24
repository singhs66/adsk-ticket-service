variable "aws_region" {
  description = "AWS region to deploy resources in."
  default     = "us-east-1"
}

variable "db_username" {
  description = "Database master username."
  type        = string
  default     = "ticket"
}

variable "db_password" {
  description = "Database master password."
  type        = string
  sensitive   = true
  default     = "nikhilticket"
}

variable "db_name" {
  description = "Database name."
  default     = "ticket-service"
}
