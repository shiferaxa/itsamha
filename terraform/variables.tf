variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name for the website"
  type        = string
  default     = "itsamha.com"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "amha-portfolio"
}

variable "contact_email" {
  description = "Address that receives contact form submissions (must be SES-verified)"
  type        = string
  default     = "amhashiferaw@gmail.com"
}
