bucket         = "afe-terraform-state-prod"
key            = "afe/prod/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "afe-terraform-lock-prod"
default_tags {
    tags = {
        Project      = "afe"
        Environment = "prod"
        CreatedBy    = "Terraform"
        SourceRepo   = "git@github.com:stevethomas15977/afe.git"
    }
}