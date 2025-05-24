#output "db_endpoint" {
#  value = aws_db_instance.postgres.endpoint
#}

output "ecr_repository_url" {
  value = aws_ecr_repository.fastapi.repository_url
}

#output "ecs_service_name" {
#  value = aws_ecs_service.fastapi.name
#}
