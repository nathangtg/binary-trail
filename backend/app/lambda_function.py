import flask
from .routes.auth_route import AuthRoute
from .routes.api_warrior import bp as api_warrior_bp
from .routes.crypto_maze import bp as crypto_maze_bp

app = flask.Flask(__name__)

# Routes registration
app.register_blueprint(AuthRoute)
app.register_blueprint(api_warrior_bp)
app.register_blueprint(crypto_maze_bp)

def lambda_handler(event, context):
    from serverless_wsgi import handle_request
    return handle_request(app, event, context)
