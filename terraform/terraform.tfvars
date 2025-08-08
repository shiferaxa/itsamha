# Amha Shiferaw Portfolio Configuration
# Update these values with your actual domain and preferences

# AWS Region (us-east-1 required for CloudFront SSL certificates)
aws_region = "us-east-1"

# Your domain name (you must own this domain and configure nameservers)
domain_name = "itsamha.com"

# Environment
environment = "prod"

# Project name
project_name = "amha-portfolio"

# Cognito callback URLs (update with your actual domain)
cognito_callback_urls = [
  "https://amhashiferaw.com/callback",
  "https://www.amhashiferaw.com/callback"
]

# Cognito logout URLs (update with your actual domain)
cognito_logout_urls = [
  "https://amhashiferaw.com",
  "https://www.amhashiferaw.com"
]