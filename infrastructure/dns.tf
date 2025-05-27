resource "aws_route53_record" "ui" {
  zone_id = var.route53_zone_id
  name    = "www.adskticket.com"
  type    = "A"

  alias {
    name                   = aws_lb.app_lb.dns_name
    zone_id                = aws_lb.app_lb.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "root" {
  zone_id = var.route53_zone_id
  name    = "adskticket.com"
  type    = "A"

  alias {
    name                   = aws_lb.app_lb.dns_name
    zone_id                = aws_lb.app_lb.zone_id
    evaluate_target_health = true
  }
}

