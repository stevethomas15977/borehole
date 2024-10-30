# afe

### Terraform State Management

export app="afe"
export env="dev"

aws s3api create-bucket --bucket $app-terraform-state-$env --region us-east-1 --profile $env

aws dynamodb --profile $env create-table \
  --table-name $app-terraform-lock-$env \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST


  ### Github Actions Runner

  https://github.com/stevethomas15977/afe/settings/actions/runners/new?arch=x64&os=linux

  https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service

  
  

