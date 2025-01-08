import flask
from .routes.auth_route import AuthRoute

app = flask.Flask(__name__)

app.register_blueprint(AuthRoute)

if __name__ == "__main__":
    app.run(debug=True)