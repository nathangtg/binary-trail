import os
from flask import Flask

from .routes.auth_route import AuthRoute
from .routes.api_warrior import bp as api_warrior_bp
from .routes.crypto_maze import bp as crypto_maze_bp

def create_app():
    app = Flask(__name__)

    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    dynamodb_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    dynamodb_endpoint = os.environ.get("DYNAMODB_ENDPOINT")
    jwt_secret = os.environ.get("JWT_SECRET")


    # Register Blueprints
    app.register_blueprint(AuthRoute)
    app.register_blueprint(api_warrior_bp)
    app.register_blueprint(crypto_maze_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
