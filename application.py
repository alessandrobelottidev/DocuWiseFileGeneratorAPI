# General
import os
import uuid

# Flask
from flask import Flask, make_response, render_template

# Dotenv
from dotenv import load_dotenv

# AWS S3 SDK
import boto3

# Pydantic models
import models
from flask_pydantic import validate

# Pdfkit for converting html to pdf
import pdfkit

# Imgkit for converting html to image
import imgkit

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

# Imgkit config
wkh2i_options = {
    'width': 1050,
    'height': 1485,
    'format': 'jpg',
    'encoding': "UTF-8",
}


@application.get("/status")
def status():
    return dict(message="OK - healthy")


@application.post("/generatePDF")
@validate()
def generate_pdf(body: models.Body):
    invoice_theme = body.fattura.theme.lower()
    html = render_template(f"{invoice_theme}.html", azienda=body.azienda, fattura=body.fattura)
    css = f"./static/{invoice_theme}PDF.css"

    pdf = pdfkit.from_string(input=html, output_path=False, css=css, options=wkh2p_options)
    pdf_id = str(uuid.uuid4())

    try:
        bucket.put_object(Body=pdf, Key=pdf_id, ContentType='application/pdf')
    except Exception as e:
        print(e)
        return make_response("", 500)

    return make_response(pdf_id, 200)


@application.post("/generateJPEG")
@validate()
def generate_jpeg(body: models.Body):
    invoice_theme = body.fattura.theme.lower()
    html = render_template(f"{invoice_theme}.html", azienda=body.azienda, fattura=body.fattura)
    css = f"./static/{invoice_theme}JPEG.css"

    image = imgkit.from_string(string=html, output_path=False, css=css, options=wkh2i_options)
    image_id = str(uuid.uuid4())

    try:
        bucket.put_object(Body=image, Key=image_id, ContentType='image/jpeg')
    except Exception as e:
        print(e)
        return make_response("", 500)

    return make_response(image_id, 200)


@application.errorhandler(404)
def page_not_found(e):
    return make_response(dict(message="404 Not Found"), 404)


@application.errorhandler(500)
def page_not_found(e):
    return make_response(dict(message="500 Internal Server Error"), 500)
