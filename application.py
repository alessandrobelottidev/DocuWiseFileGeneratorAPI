from flask import Flask, make_response

# Pdfkit for converting html to pdf
import pdfkit

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