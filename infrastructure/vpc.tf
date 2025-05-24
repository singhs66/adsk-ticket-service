resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"
}

#resource "aws_subnet" "public_2" {
#  vpc_id                  = aws_vpc.main.id
#  cidr_block              = "10.0.0.0/20"
#  map_public_ip_on_launch = true
#  availability_zone       = "${var.aws_region}a"
#}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.16.0/20"
  map_public_ip_on_launch = false
  availability_zone       = "${var.aws_region}b"
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}
