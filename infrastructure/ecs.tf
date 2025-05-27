resource "aws_ecs_cluster" "main" {
  name = "fastapi-cluster"
}

resource "aws_cloudwatch_log_group" "ecs_fastapi" {
  name              = "/ecs/fastapi"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "fastapi" {
  family                   = "fastapi-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  container_definitions    = jsonencode([
    {
      name      = "fastapi"
      image     = aws_ecr_repository.fastapi.repository_url
      essential = true
      portMappings = [{ containerPort = 8000, hostPort = 8000 }]
      environment = [
        {
          name  = "DB_PASSWORD_PARAM_NAME"
          value = var.db_password_param_name
        },
        {
          name  = "AWS_REGION"
          value = var.aws_region
        },
        {
          name  = "REDIS_URL"
          value = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:6379/0"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_fastapi.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      secrets = [
        {
          name      = "DB_PASSWORD"
          valueFrom = aws_ssm_parameter.db_password.arn
        },
        {
          name      = "SLACK_WEBHOOK_URL"
          valueFrom = aws_ssm_parameter.slack_webhook_url.arn
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "fastapi" {
  name            = "fastapi-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.fastapi.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [aws_subnet.public.id]
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.ui_tg.arn
    container_name   = "fastapi"
    container_port   = 8000
  }
}
