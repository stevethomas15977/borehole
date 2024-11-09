# output "load_balancer_dns" {
#   description = "The DNS name of the Lightsail Load Balancer"
#   value       = aws_lightsail_lb.lb.dns_name
# }

# output "instance_public_ip" {
#   description = "The public IP of the Lightsail instance"
#   value       = aws_lightsail_static_ip.static-ip.ip_address
# }

# output "application_url" {
#   description = "The full URL to access the application"
#   value       = format("https://%s", aws_lightsail_lb.lb.dns_name)
# }

# output "ssl_certificate_arn" {
#   description = "The ARN of the SSL certificate attached to the Load Balancer"
#   value       = aws_lightsail_lb_certificate.certificate.arn
# }
