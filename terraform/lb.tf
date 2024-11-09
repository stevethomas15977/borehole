# # Lightsail Static IP
# resource "aws_lightsail_static_ip" "static-ip" {
#   name = "${var.app}-static-ip"
# }

# # Attach Static IP to Instance
# resource "aws_lightsail_static_ip_attachment" "static-ip-attachment" {
#   instance_name  = aws_lightsail_instance.instance.name
#   static_ip_name = aws_lightsail_static_ip.static-ip.name
#   depends_on = [aws_lightsail_static_ip.static-ip ]
# }

# # Lightsail Load Balancer
# resource "aws_lightsail_lb" "lb" {
#   name              = "lb"
#   health_check_path = "/health"
#   instance_port     = 80
# }

# # # Attach SSL Certificate to Load Balancer
# resource "aws_lightsail_lb_certificate" "certificate" {
#   name        = "certificate"
#   lb_name     = aws_lightsail_lb.lb.name
#   domain_name = "${var.env}.softwarelikeyou.com"
#   depends_on = [ aws_lightsail_lb.lb ]
# }

# resource "aws_lightsail_lb_certificate_attachment" "lb-certificate-attachment" {
#   lb_name          = aws_lightsail_lb.lb.name
#   certificate_name = aws_lightsail_lb_certificate.certificate.name
# }

# # # Attach Instance to Load Balancer
# resource "aws_lightsail_lb_attachment" "lb-attachment" {
#   lb_name       = aws_lightsail_lb.lb.name
#   instance_name = aws_lightsail_instance.instance.name
# }
