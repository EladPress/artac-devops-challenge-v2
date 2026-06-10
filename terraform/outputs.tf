output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app.public_ip
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.app.id
}

output "app_url" {
  description = "URL to access the application"
  value       = "http://${aws_instance.app.public_ip}:${var.app_port}"
}

output "ssm_command" {
  description = "Command to open a shell on the instance via SSM Session Manager"
  value       = "aws ssm start-session --target ${aws_instance.app.id} --region ${var.aws_region}"
}
