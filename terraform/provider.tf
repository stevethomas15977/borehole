provider "aws" {
  
}

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
  
  backend "s3" {}
}
