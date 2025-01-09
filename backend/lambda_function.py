from app import create_app
from serverless_wsgi import handle_request

# Create the Flask app
app = create_app()

def lambda_handler(event, context):
    return handle_request(app, event, context)
