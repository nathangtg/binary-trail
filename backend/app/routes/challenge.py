import flask
from flask import request, jsonify, Blueprint
from ..controllers.challenge_controller import ChallengeController

ChallengeRoute = Blueprint("ChallengeRoute", __name__)

@ChallengeRoute.route("/challenges", methods=["GET"])
def get_all_challenges():
    challenges = ChallengeController().get_all_challenges()
    return jsonify(challenges), 200

@ChallengeRoute.route("/challenges/<challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    challenge = ChallengeController().get_challenge(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404
    return challenge

@ChallengeRoute.route("/challenges/i-am-too-lazy-to-create-iam-middleware", methods=["POST"])
def create_challenge():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is missing"}), 400
    
    try:
        challenge = ChallengeController().create_challenge(data)
        return {
            "message": "Challenge created successfully",
            "challenge": challenge
        }
    except ValueError as e:
        return jsonify({"error": str(e)}), 400