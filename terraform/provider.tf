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
    bucket         = "${locals.app}-terraform-state-${locals.env}" 
    key            = "${locals.env}/terraform.tfstate"      
    region         = "${locals.region}"                      
    encrypt        = true
    dynamodb_table = "${locals.app}-terraform-lock-${locals.env}"
  }
}

provider "aws" {
    region = "${locals.region}"
    default_tags {
        tags = {
        Project      = "${locals.app}"
        Environment = "${locals.env}"
        CreatedBy    = "Terraform"
        SourceRepo   = "git@github.com:${locals.github_org}/${locals.app}.git"
        }
    }
}