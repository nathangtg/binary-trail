import flask
from .routes.auth_route import AuthRoute
from .routes.api_warrior import bp as api_warrior_bp

app = flask.Flask(__name__)

app.register_blueprint(AuthRoute)
app.register_blueprint(api_warrior_bp)

if __name__ == "__main__":
    app.run(debug=True)