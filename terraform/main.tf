terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAT2U3KSJOODOWKUF2"
  secret_key = "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"
}

resource "aws_security_group" "terraform-sg" {
  name = "terraform-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "deploy_server" {
  ami           = "ami-0d527b8c289b4af7f"
  instance_type = "t2.micro"
  key_name      = "jenkins"
  vpc_security_group_ids = [aws_security_group.terraform-sg.id]

  tags = {
    Name = "DeployServer"
  }
}
