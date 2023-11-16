import smtplib
import json
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Send email
def sendEmails(subject, body, to_email):
    """Send emails"""
    # email server
    from_email = ''
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = from_email
    smtp_password = ''
    # data email setup
    to_addr = to_email
    data_msg = f"From: {from_email}\r\nTo: {to_addr}\r\nSubject: {subject}\r\n\r\n{body}"
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_addr.split(','), data_msg)

def is_valid_email(email):
    """Check if the given email is a valid email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def lambda_handler(event, context):
    # Get the username, password, and company name from the request body
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': 'Bad request: missing request body'
        }

    request_body = event['body']
    if not request_body:
        return {
            'statusCode': 400,
            'body': 'Bad request: empty request body'
        }

    try:
        body_dict = json.loads(request_body)
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': f'Bad request: invalid request body ({e})'
        }

    if 'formtype' not in body_dict:
        return {
            'statusCode': 400,
            'body': 'Bad request: missing parameter(s)'
        }

    form_type = str(body_dict['formtype'])
    if not form_type:
        return {
            'statusCode': 400,
            'body': 'Bad request: missing parameter(s)'
        }

    email = str(body_dict['email'])
    if not is_valid_email(email):
        return {
            'statusCode': 400,
            'body': 'Invalid email: not a valid email address'
        }

    subject = ''
    body = ''

    # Contact form
    if form_type == 'contact':
        subject = 'contact form'
        name = str(body_dict['name'])
        message = str(body_dict['message'])
        # Ensure that the values are not blank strings
        if not name:
            return {
                'statusCode': 400,
                'body': 'Invalid name: name cannot be blank'
            }
        if not message:
            return {
                'statusCode': 400,
                'body': 'Invalid message: message cannot be blank'
            }
        body = f"email: {email}\r\nname: {name}\r\nmessage: {message}"

    # Ensure that the values are not blank strings
    if not subject or not body:
        return {
            'statusCode': 400,
            'body': 'Bad request: missing parameter(s)'
        }

    # Send emails
    sendEmails(subject, body, email)

    # Return a success message
    return {
        'statusCode': 200,
        'body': 'Form submitted'
    }
