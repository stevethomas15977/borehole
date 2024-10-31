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

variable "gh_pat" {
    description = "GitHub Personal Access Token"
    type        = string
}