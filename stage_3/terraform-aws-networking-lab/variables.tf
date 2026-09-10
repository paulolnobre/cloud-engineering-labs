variable "aws_region" {
  description = "AWS region where the lab resources will be created."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z]{2}(-[a-z]+)+-[0-9]+$", var.aws_region))
    error_message = "aws_region must be a valid AWS region name, such as us-east-1."
  }
}

variable "project_name" {
  description = "Value used in resource names and in the Project cost-allocation tag."
  type        = string
  default     = "terraform-aws-networking-lab"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{2,31}$", var.project_name))
    error_message = "project_name must contain 3-32 lowercase letters, numbers, or hyphens."
  }
}

variable "environment" {
  description = "Environment tag used to identify the lifecycle and cost context of the resources."
  type        = string
  default     = "lab"

  validation {
    condition     = contains(["lab", "dev", "test"], var.environment)
    error_message = "environment must be one of: lab, dev, test."
  }
}

variable "vpc_cidr" {
  description = "Private IPv4 CIDR block assigned to the VPC."
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "vpc_cidr must be a valid IPv4 CIDR block."
  }
}

variable "public_subnet_cidr" {
  description = "IPv4 CIDR block assigned to the public subnet; it must fit inside vpc_cidr."
  type        = string
  default     = "10.0.1.0/24"

  validation {
    condition     = can(cidrnetmask(var.public_subnet_cidr))
    error_message = "public_subnet_cidr must be a valid IPv4 CIDR block."
  }
}

variable "instance_type" {
  description = "Small x86 EC2 instance type used by the lab. Restricting the allowed values reduces accidental cost."
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro"], var.instance_type)
    error_message = "instance_type must be either t2.micro or t3.micro."
  }
}

variable "ssh_allowed_cidr" {
  description = "Optional trusted IPv4 CIDR allowed to reach SSH. Keep null for no inbound access; when used, prefer your public IP with /32."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition     = var.ssh_allowed_cidr == null || can(cidrnetmask(var.ssh_allowed_cidr))
    error_message = "ssh_allowed_cidr must be null or a valid IPv4 CIDR block, preferably a /32."
  }
}

variable "key_name" {
  description = "Optional name of an existing EC2 key pair. Required when ssh_allowed_cidr is set."
  type        = string
  default     = null
  nullable    = true
}
