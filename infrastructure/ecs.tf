#resource "aws_ecs_cluster" "main" {
#  name = "fastapi-cluster"
#}
#
#resource "aws_ecs_task_definition" "fastapi" {
#  family                   = "fastapi-task"
#  network_mode             = "awsvpc"
#  requires_compatibilities = ["FARGATE"]
#  cpu                      = "256"
#  memory                   = "512"
#  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
#  container_definitions    = jsonencode([
#    {
#      name      = "fastapi"
#      image     = aws_ecr_repository.fastapi.repository_url
#      essential = true
#      portMappings = [{ containerPort = 80, hostPort = 80 }]
#      environment = []
#    }
#  ])
#}
#
#resource "aws_ecs_service" "fastapi" {
#  name            = "fastapi-service"
#  cluster         = aws_ecs_cluster.main.id
#  task_definition = aws_ecs_task_definition.fastapi.arn
#  desired_count   = 1
#  launch_type     = "FARGATE"
#  network_configuration {
#    subnets          = [aws_subnet.public.id]
#    security_groups  = [aws_security_group.ecs.id]
#    assign_public_ip = true
#  }
#  depends_on = [aws_db_instance.postgres]
#}
