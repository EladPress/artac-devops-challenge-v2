terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Resolves the region-specific equivalent of ami-0c7217cdde317cfec
# (Ubuntu 22.04 LTS, amd64, owned by Canonical) so the AMI is portable
# across regions instead of being hardcoded to a us-east-1 ID.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-sg"
  description = "Security group for ${var.project_name}"

  ingress {
    description = "HTTP access to application"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = var.app_allowed_cidrs
  }

  # No SSH ingress: instance access is via SSM Session Manager (outbound 443 only).

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}-sg"
    Project = var.project_name
  }
}

# IAM role granting the instance SSM access, so operators connect via
# Session Manager instead of SSH. AmazonSSMManagedInstanceCore is the AWS
# managed policy that lets the SSM Agent register and broker sessions.
resource "aws_iam_role" "ssm" {
  name = "${var.project_name}-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })

  tags = {
    Name    = "${var.project_name}-ssm-role"
    Project = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ssm.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ssm" {
  name = "${var.project_name}-ssm-profile"
  role = aws_iam_role.ssm.name
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  iam_instance_profile   = aws_iam_instance_profile.ssm.name
  vpc_security_group_ids = [aws_security_group.app.id]

  user_data = templatefile("${path.module}/user-data.sh", {
    docker_image = var.docker_image
    app_port     = var.app_port
  })

  # Root volume only (stateless app, no separate data volume). Right-sized for
  # OS + Docker + image, on gp3, encrypted at rest.
  root_block_device {
    volume_size = 10
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name    = "${var.project_name}-server"
    Project = var.project_name
  }
}
