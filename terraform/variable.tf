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

variable "ghpat" {
    description = "GitHub Personal Access Token"
    type        = string
}

variable "appsecret" {
    description = "Application secret"
    type        = string
}

variable "env" {
    description = "Environment"
    type        = string
}

variable "s3_bucket" {
    description = "S3 bucket name"
    type        = string
}   