# Create a Lightsail bucket
resource "aws_lightsail_bucket" "bucket" {
  name      = "${var.app}-bucket"
  bundle_id = "small_1_0"
}

# Create an access key for the Lightsail bucket
resource "aws_lightsail_bucket_access_key" "bucket-access-key" {
  bucket_name = aws_lightsail_bucket.bucket.name
}