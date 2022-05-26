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
  region     = "eu-central-1"
  access_key = "AKIA52X6EA3KVEXDSPYJ"
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
  key_name      = "jk"
  vpc_security_group_ids = [aws_security_group.terraform-sg.id]

  tags = {
    Name = "DeployServer"
  }
}
