# Write the private key to a temporary file for SSH
resource "null_resource" "write_ssh_key" {
  depends_on = [ aws_lightsail_key_pair.key-pair ]
  provisioner "local-exec" {
    command = <<EOT
      echo '${aws_lightsail_key_pair.key-pair.private_key}' > ./lightsail_key.pem
      chmod 400 ./lightsail_key.pem
    EOT
  }
}

# Wait for the user_data script to complete
resource "null_resource" "wait_for_user_data" {
  depends_on = [aws_lightsail_instance.instance, 
                null_resource.write_ssh_key]

  provisioner "local-exec" {
    command = <<EOT
      while ! ssh -i ./lightsail_key.pem -o "StrictHostKeyChecking=no" ubuntu@${aws_lightsail_instance.instance.public_ip_address} 'test -e /var/log/user_data_complete && echo true'; do
        echo "Waiting for user_data script to complete..."
        sleep 10
      done
      echo "User data script completed."
    EOT
  }

  # Clean up the key after use
  provisioner "local-exec" {
    when    = destroy
    command = "rm -f ./lightsail_key.pem"
  }
}

# Lightsail Static IP
resource "aws_lightsail_static_ip" "static-ip" {
  name = "${var.app}-static-ip"
}

# Attach Static IP to Instance
resource "aws_lightsail_static_ip_attachment" "static-ip-attachment" {
  instance_name  = aws_lightsail_instance.instance.name
  static_ip_name = aws_lightsail_static_ip.static-ip.name
  depends_on = [aws_lightsail_static_ip.static-ip ]
}

# Lightsail Load Balancer
resource "aws_lightsail_lb" "lb" {
  name              = "lb"
  health_check_path = "/health"
  instance_port     = 80
}

# # Attach SSL Certificate to Load Balancer
resource "aws_lightsail_lb_certificate" "afe-dev-softwarelikeyou-com" {
  name        = "afe"
  lb_name     = aws_lightsail_lb.lb.name
  domain_name = "afe-dev.softwarelikeyou.com"
  depends_on = [ aws_lightsail_lb.lb ]
}

resource "aws_lightsail_lb_certificate_attachment" "lb-certificate-attachment" {
  lb_name          = aws_lightsail_lb.lb.name
  certificate_name = aws_lightsail_lb_certificate.afe-dev-softwarelikeyou-com.name
}

# # Attach Instance to Load Balancer
resource "aws_lightsail_lb_attachment" "lb-attachment" {
  lb_name       = aws_lightsail_lb.lb.name
  instance_name = aws_lightsail_instance.instance.name
  depends_on = [null_resource.wait_for_user_data]
}
