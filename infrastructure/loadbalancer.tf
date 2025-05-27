resource "aws_lb" "app_lb" {
  name               = "ticket-service-lb"
  internal           = false
  load_balancer_type = "application"
  subnets            = [aws_subnet.public.id, aws_subnet.private.id]

  security_groups = [aws_security_group.lb_sg_v2.id]
}

resource "aws_lb_target_group" "ui_tg" {
  name     = "ticket-service-tg-8000"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  target_type = "ip"

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200-399"
  }
}

resource "aws_acm_certificate" "alb_cert" {
  domain_name               = "adskticket.com"
  subject_alternative_names = ["www.adskticket.com"]
  validation_method         = "DNS"
}

resource "aws_route53_record" "alb_cert_validation" {
  count   = length(aws_acm_certificate.alb_cert.domain_validation_options)
  zone_id = var.route53_zone_id
  name    = tolist(aws_acm_certificate.alb_cert.domain_validation_options)[count.index].resource_record_name
  type    = tolist(aws_acm_certificate.alb_cert.domain_validation_options)[count.index].resource_record_type
  records = [tolist(aws_acm_certificate.alb_cert.domain_validation_options)[count.index].resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "alb_cert_validation" {
  certificate_arn         = aws_acm_certificate.alb_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.alb_cert_validation : record.fqdn]
}

# HTTPS listener for ALB
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.alb_cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ui_tg.arn
  }
}

# HTTP listener for ALB (redirect to HTTPS)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}
