import json
import boto3
import os
from datetime import datetime

def handler(event, context):
    """
    Lambda function to handle contact form submissions
    """
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }
    
    # Handle preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight'})
        }
    
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in body or not body[field].strip():
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': f'Missing required field: {field}'
                    })
                }
        
        # Extract form data
        name = body['name'].strip()
        email = body['email'].strip()
        message = body['message'].strip()
        subject = body.get('subject', 'Contact Form Submission').strip()
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Invalid email address'
                })
            }
        
        # Create timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # In a real implementation, you would:
        # 1. Send email via SES
        # 2. Store in DynamoDB
        # 3. Send to SNS topic
        
        # For demo purposes, we'll just log and return success
        print(f"Contact form submission received:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print(f"Timestamp: {timestamp}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Thank you for your message! I will get back to you soon.',
                'timestamp': timestamp
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'error': 'Invalid JSON in request body'
            })
        }
    
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }
