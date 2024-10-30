terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.72.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.1.0"
    }
  }

  backend "s3" {
    bucket         = "${var.app}-terraform-state-${var.env}" 
    key            = "${var.env}/terraform.tfstate"      
    region         = "${var.region}"                      
    encrypt        = true
    dynamodb_table = "${var.app}-terraform-lock-${var.env}"
  }
}

provider "aws" {
    region = "${var.region}"
    default_tags {
        tags = {
        Project      = "${var.app}"
        Environment = "${var.env}"
        CreatedBy    = "Terraform"
        SourceRepo   = "git@github.com:${var.github_org}/${var.app}.git"
        }
    }
}