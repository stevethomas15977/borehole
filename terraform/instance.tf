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
        export GH_PAT="${var.ghpat}"
        export APP_SECRET="${var.appsecret}"
        export APP="afe"
        export ENV="prod"
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
        mkdir -p $GEOJSON_PATH
        mkdir -p $PROJECTS_PATH

        # Clone the GitHub repository
        mkdir -p /tmp/afe
        cd /tmp/afe
        git clone https://$GH_PAT@github.com/stevethomas15977/afe.git .
        git checkout main

        cp -R /tmp/afe/app/* $AFE_PATH
        cp -R /tmp/afe/plss/* $GEOJSON_PATH

        # Adjust permissions
        chown -R ubuntu:ubuntu $AFE_PATH

        cd $APP_PATH

        # Set up the environment variables
        export HTTP_PORT=80
        export PASSWORD=$APP_SECRET
        export ENV="prod"

        sh -c "cat > $APP_PATH/.env" <<EOG
        VERSION="1.7.0"
        ENV="$ENV"
        APP="$APP"
        APP_ROOT="$APP_ROOT"
        AFE_PATH=$AFE_PATH
        APP_PATH="$APP_PATH"
        PROJECTS_PATH="$PROJECTS_PATH"
        GEOJSON_PATH="$AFE_PATH/$S3_FOLDER_NAME"
        CODEVELOPMENT_FIRST_PRODUCTION_DATE_DAYS_THRESHOLD=180
        MAX_DISTANCE_THRESHOLD=8000
        HORIZONTAL_DISTANCE_THRESHOLD=1600
        VERTICAL_DISTANCE_THRESHOLD=500
        LATERAL_LENGTH_THRESHOLD=.8
        HYPOTENUSE_DISTANCE_THRESHOLD=1800
        DEPTH_DISTANCE_THRESHOLD=1500
        TEXAS_LAND_SURVEY_SYSTEM_DATABASE="texas_land_survey_system.db"
        NEW_MEXICO_LAND_SURVEY_SYSTEM_DATABASE="new_mexico_land_survey_system.db"
        NM_SECTION_COLUMN="FRSTDIVLAB"
        TX_ABSTRACT_COLUMN="ABSTRACT_L"
        USERNAME="afe-admin"
        PASSWORD="$APP_SECRET"
        S3_BUCKET_NAME="$S3_BUCKET_NAME"
        GEOJSON_PATH="$GEOJSON_PATH"
        EOG

        # Set up the virtual environment and install dependencies
        python3 -m venv venv
        . venv/bin/activate
        pip install pipenv
        pipenv sync

    EOF
}