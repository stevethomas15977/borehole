bucket         = "afe-terraform-state-dev"
key            = "afe/dev/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "afe-terraform-lock-dev"
default_tags {
    tags = {
        Project      = "afe"
        Environment = "dev"
        CreatedBy    = "Terraform"
        SourceRepo   = "git@github.com:stevethomas15977/afe.git"
    }
}
