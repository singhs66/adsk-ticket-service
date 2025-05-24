resource "aws_db_subnet_group" "default" {
  name       = "main-db-subnet-group"
  subnet_ids = [aws_subnet.public.id, aws_subnet.private.id]
}

resource "aws_db_instance" "postgres" {
  identifier             = "ticketdb"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "17.2"
  instance_class         = "db.t3.micro"
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot    = true
  publicly_accessible    = true
}
