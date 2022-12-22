# General
import os

# Flask
from flask import Flask, make_response

# Dotenv
from dotenv import load_dotenv

# AWS S3 SDK
import boto3

# Pydantic models
import models
from flask_pydantic import validate

# Pdfkit for converting html to pdf
import pdfkit

# Load environment variables
load_dotenv()

# AWS S3 setup
s3 = boto3.resource(
    service_name='s3',
    region_name=os.environ.get('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)
bucket = s3.Bucket(os.environ.get('AWS_BUCKET_NAME'))


# Create a new Flask app instance
application = Flask(__name__)

# Pdfkit config
wkh2p_options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
}


@application.get("/status")
def status():
    return dict(message="OK - healthy")


@application.get("/test/pdf")
def test_pdf():
    html = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Test</title>
        </head>
        <body>
            <h1>Test</h1>
            <p>Test</p>
        </body>
    </html>
    """
    response = make_response(pdfkit.from_string(html, False, options=wkh2p_options))

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=test.pdf'

    return response