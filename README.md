# Personal Portfolio Website

My personal portfolio website built on AWS infrastructure. This project demonstrates cloud engineering skills through practical implementation of various AWS services.

[MY SITE](https://itsamha.com)

## Architecture

The site uses these AWS services:
- **Terraform**: Infrastructure as Code
- **S3**: Static website hosting
- **CloudFront**: Content delivery network
- **VPC/Networking**: Custom networking setup
- **Lambda**: Serverless backend functions
- **API Gateway**: REST API endpoints

## Infrastructure Components

- S3 bucket for static website hosting
- CloudFront distribution for global content delivery
- Lambda functions for API endpoints
- VPC with public and private subnets
- API Gateway for REST API management

## Deployment

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

See `docs/DEPLOYMENT.md` for detailed instructions.

## Project Structure

```
├── terraform/           # Infrastructure as Code
├── website/            # Static website files
├── lambda/             # Serverless functions
└── docs/               # Documentation
```
