resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "ticket-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.redis.id]
  engine_version       = "7.0"
  apply_immediately    = true
  tags = {
    Name = "ticket-redis"
  }
}
