# Variables for S3 bucket and DynamoDB table names based on environment
variable "env" {
    description = "Environment (e.g., dev, prod)"
    type        = string
    default     = "dev"
}

variable "region" {
    description = "AWS region"
    type        = string
    default     = "us-east-1"
}

variable "app" {
    description = "Application name"
    type        = string
     default     = "afe"
}

variable "github_org" {
    description = "GitHub organization"
    type        = string
    default     = "stevethomas15977"
}