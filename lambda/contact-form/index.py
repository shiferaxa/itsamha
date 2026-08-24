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

        # Honeypot: the hidden "company" field is never filled by humans.
        # Return a fake success so bots don't learn they were caught.
        if body.get('company', '').strip():
            print("Honeypot triggered, dropping submission")
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'message': 'Thank you for your message! I will get back to you soon.',
                    'success': True
                })
            }

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
        
        # Create timestamp and unique ID
        timestamp = datetime.utcnow().isoformat()
        import uuid
        submission_id = str(uuid.uuid4())
        
        # Prepare submission data
        submission_data = {
            'id': submission_id,
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': timestamp,
            'source_ip': event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown'),
            'user_agent': event.get('headers', {}).get('User-Agent', 'unknown')
        }
        
        # Log the submission (CloudWatch keeps a copy even if email fails)
        print(f"Contact form submission received:")
        print(f"ID: {submission_id}")
        print(f"From: {name} <{email}>")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print(f"Timestamp: {timestamp}")
        print(f"Source IP: {submission_data['source_ip']}")

        # Email the submission via SES. The contact address is both the
        # verified sender identity and the recipient; Reply-To goes to the
        # submitter so replying in the inbox just works.
        contact_email = os.environ.get('CONTACT_EMAIL')
        if contact_email:
            try:
                ses = boto3.client('ses')
                ses.send_email(
                    Source=contact_email,
                    Destination={'ToAddresses': [contact_email]},
                    ReplyToAddresses=[email],
                    Message={
                        'Subject': {'Data': f"[itsamha.com] {subject}"},
                        'Body': {'Text': {'Data': (
                            f"From: {name} <{email}>\n"
                            f"Time: {timestamp}\n"
                            f"Source IP: {submission_data['source_ip']}\n"
                            f"Submission ID: {submission_id}\n\n"
                            f"{message}"
                        )}}
                    }
                )
                print(f"Email sent to {contact_email}")
            except Exception as ses_error:
                # Submission is still in the logs; don't fail the request
                print(f"SES send failed: {ses_error}")

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Thank you for your message! I will get back to you soon.',
                'success': True,
                'submission_id': submission_id,
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