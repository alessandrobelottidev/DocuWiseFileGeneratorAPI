from flask import Flask

# Create a new Flask app instance
application = Flask(__name__)


@application.get("/status")
def status():
    return dict(message="OK - healthy")
