output "vpc_id" {
  description = "ID of the VPC created for the lab."
  value       = aws_vpc.lab.id
}

output "public_subnet_id" {
  description = "ID of the public subnet created for the lab."
  value       = aws_subnet.public.id
}

output "route_table_id" {
  description = "ID of the route table associated with the public subnet."
  value       = aws_route_table.public.id
}

output "security_group_id" {
  description = "ID of the security group attached to the EC2 instance."
  value       = aws_security_group.ec2.id
}

output "ec2_instance_id" {
  description = "ID of the lab EC2 instance."
  value       = aws_instance.lab.id
}

output "ec2_public_ip" {
  description = "Public IPv4 address assigned to the EC2 instance. Inbound access is disabled unless SSH is explicitly configured."
  value       = aws_instance.lab.public_ip
}
