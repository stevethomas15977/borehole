output "aws_lightsail_bucket" {
    description = "ARN of the aws lightsail bucket name"
    value = aws_lightsail_bucket.bucket.name
}