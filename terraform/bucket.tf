# Create a Lightsail bucket
resource "aws_lightsail_bucket" "bucket" {
  name      = "${var.app}-bucket"
  bundle_id = "small_1_0"
}

# Create an access key for the Lightsail bucket
resource "aws_lightsail_bucket_access_key" "bucket-access-key" {
  bucket_name = aws_lightsail_bucket.bucket.name
}

resource "null_resource" "upload_new_mexico_land_survey_syste_to_s3" {
  provisioner "local-exec" {
    command = "AWS_DEFAULT_REGION=us-east-1; AWS_ACCESS_KEY_ID=${aws_lightsail_bucket_access_key.offset-well-identification-lightsail-bucket-access-key.access_key_id}; AWS_SECRET_ACCESS_KEY=${aws_lightsail_bucket_access_key.offset-well-identification-lightsail-bucket-access-key.secret_access_key}; aws s3 cp new_mexico_land_survey_system.db s3://${aws_lightsail_bucket.offset-well-identification-lightsail-bucket.name}/new_mexico_land_survey_system.db;"
  }

  # Ensure the S3 bucket is created before the upload
  depends_on = [ aws_lightsail_bucket.bucket,
                 aws_lightsail_bucket_access_key.bucket-access-key ]
}

resource "null_resource" "upload_texas_land_survey_system_to_s3" {
  provisioner "local-exec" {
    command = "AWS_DEFAULT_REGION=us-east-1; AWS_ACCESS_KEY_ID=${aws_lightsail_bucket_access_key.offset-well-identification-lightsail-bucket-access-key.access_key_id}; AWS_SECRET_ACCESS_KEY=${aws_lightsail_bucket_access_key.offset-well-identification-lightsail-bucket-access-key.secret_access_key}; aws s3 cp texas_land_survey_system.db s3://${aws_lightsail_bucket.offset-well-identification-lightsail-bucket.name}/texas_land_survey_system.db;"
  }

  # Ensure the S3 bucket is created before the upload
  depends_on = [ aws_lightsail_bucket.bucket,
                 aws_lightsail_bucket_access_key.bucket-access-key ]
}

