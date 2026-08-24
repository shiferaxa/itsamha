import {
  to = aws_s3_bucket.website
  id = "itsamha.com"
}
import {
  to = aws_s3_bucket_website_configuration.website
  id = "itsamha.com"
}
import {
  to = aws_s3_bucket_versioning.website
  id = "itsamha.com"
}
import {
  to = aws_s3_bucket_server_side_encryption_configuration.website
  id = "itsamha.com"
}
import {
  to = aws_s3_bucket_policy.website
  id = "itsamha.com"
}
import {
  to = aws_s3_bucket_public_access_block.website
  id = "itsamha.com"
}
import {
  to = aws_cloudfront_origin_access_control.website
  id = "ETU9H1RSJIEWL"
}
import {
  to = aws_cloudfront_distribution.website
  id = "E1RT76ETYBB5J6"
}

# Pass 2: Lambda + API Gateway
import {
  to = aws_iam_role.lambda_role
  id = "amha-portfolio-lambda-role"
}
import {
  to = aws_iam_role_policy_attachment.lambda_basic_execution
  id = "amha-portfolio-lambda-role/arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
import {
  to = aws_lambda_function.contact_form
  id = "amha-portfolio-contact-form"
}
import {
  to = aws_lambda_permission.contact_form_api
  id = "amha-portfolio-contact-form/AllowExecutionFromAPIGateway"
}
import {
  to = aws_api_gateway_rest_api.main
  id = "qoc5759x8c"
}
import {
  to = aws_api_gateway_resource.contact
  id = "qoc5759x8c/mnoa4c"
}
import {
  to = aws_api_gateway_method.contact_post
  id = "qoc5759x8c/mnoa4c/POST"
}
import {
  to = aws_api_gateway_integration.contact_form
  id = "qoc5759x8c/mnoa4c/POST"
}
import {
  to = aws_api_gateway_method.contact_options
  id = "qoc5759x8c/mnoa4c/OPTIONS"
}
import {
  to = aws_api_gateway_integration.contact_options
  id = "qoc5759x8c/mnoa4c/OPTIONS"
}
import {
  to = aws_api_gateway_method_response.contact_options
  id = "qoc5759x8c/mnoa4c/OPTIONS/200"
}
import {
  to = aws_api_gateway_integration_response.contact_options
  id = "qoc5759x8c/mnoa4c/OPTIONS/200"
}
import {
  to = aws_api_gateway_deployment.main
  id = "qoc5759x8c/wdfa9j"
}
import {
  to = aws_api_gateway_stage.main
  id = "qoc5759x8c/prod"
}
