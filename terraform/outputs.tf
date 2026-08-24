output "website_url" {
  description = "Website URL"
  value       = "https://${var.domain_name}"
}

output "cloudfront_distribution_id" {
  description = "CloudFront Distribution ID"
  value       = aws_cloudfront_distribution.website.id
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.website.bucket
}

output "api_gateway_url" {
  description = "API Gateway URL"
  value       = aws_api_gateway_stage.main.invoke_url
}
