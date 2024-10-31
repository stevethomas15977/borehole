# Create a new Lightsail Key Pair
resource "aws_lightsail_key_pair" "key-pair" {
  name = "${var.app}-key-pair"
}

# Lightsail Instance
resource "aws_lightsail_instance" "instance" {
  name                  = "${var.app}-instance"
    availability_zone   = "us-east-1a"
    blueprint_id        = "ubuntu_24_04"
    bundle_id           = "medium_3_0" 
    key_pair_name       = aws_lightsail_key_pair.key-pair.name
    user_data = <<-EOF
        #!/bin/bash
        apt-get update -y
        sudo apt-get install -y unzip jq python3-pip python3-dev python3-venv pipx nginx apache2-utils -y

        # Install pipenv
        pipx ensurepath
        pipx install pipenv

        # Install AWS CLI
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        rm -rf aws
        rm awscliv2.zip

        aws configure set aws_access_key_id ${aws_lightsail_bucket_access_key.bucket-access-key.access_key_id} --profile lightsail
        aws configure set aws_secret_access_key ${aws_lightsail_bucket_access_key.bucket-access-key.secret_access_key} --profile lightsail
        aws configure set region "us-east-1" --profile lightsail

        # Set up the environment variables
        export GH_PATH="${var.ghpat}"
        echo "export GH_PATH=${var.ghpat}"
        export APP="afe"
        export APP_ROOT="/home/ubuntu"
        export AFE_PATH=$APP_ROOT/afe
        export APP_PATH=$AFE_PATH/app
        export S3_BUCKET_NAME="afe-plss"
        export S3_FOLDER_NAME="geojson"
        export GEOJSON_PATH=$AFE_PATH/$S3_FOLDER_NAME
        export PROJECTS_PATH=$AFE_PATH/projects

        # Create project directory
        mkdir -p $AFE_PATH
        mkdir -p $APP_PATH
        mkdir -p $PROJECTS_PATH

        # Clone the GitHub repository
        cd /tmp
        git clone https://$GH_PATH@github.com/stevethomas15977/afe.git
        git checkout main

        cp -R /tmp/afe/app/* $AFE_PATH
        cp -R /tmp/afe/plss/* $GEOJSON_PATH

        # Adjust permissions
        chown -R ubuntu:ubuntu $AFE_PATH

    EOF
}