output "vpc_id" {
  value = aws_vpc.lab.id
}

output "vpc_cidr_block" {
  value = aws_vpc.lab.cidr_block
}

output "public_subnet_cidr" {
  value = aws_subnet.public_a.cidr_block
}

output "internet_gateway_id" {
  value = aws_internet_gateway.lab.id
}