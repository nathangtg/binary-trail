from flask import request, jsonify, Blueprint
from ..controllers.auth_controller import AuthController

AuthRoute = Blueprint("AuthRoute", __name__)

@AuthRoute.route("/register", methods=["POST"])
def register_user():
    data = request.json
    if not data:
        return jsonify({"error": "Request body is missing"}), 400
    
    try:
        user = AuthController().register_user(data)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@AuthRoute.route("/login", methods=["POST"])
def login_user():
    data = request.json
    if not data:
        return jsonify({"error": "Request body is missing"}), 400
    
    try:
        user = AuthController().login_user(data)
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400