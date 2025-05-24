resource "aws_route53_zone" "dinemeta" {
  name = "dinemeta.com"
}

resource "aws_route53_record" "ui" {
  zone_id = aws_route53_zone.dinemeta.zone_id
  name    = "www.dinemeta.com/*"
  type    = "A"

  alias {
    name                   = aws_lb.app_lb.dns_name
    zone_id                = aws_lb.app_lb.zone_id
    evaluate_target_health = true
  }
}

