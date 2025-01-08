from flask import Blueprint, request, jsonify
from ..controllers.phase_1 import Phase1Controller
from ..utils.auth import require_auth
from ..utils.rate_limit import rate_limit

bp = Blueprint('phase1', __name__, url_prefix='/phase1')
controller = Phase1Controller()

@bp.route('/begin', methods=['GET'])
@require_auth
def begin_challenge():
    try:
        user_email = request.user.email
        result = controller.create_challenge(user_email)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/step/<challenge_id>', methods=['POST'])
@require_auth
@rate_limit(max_requests=5, window_seconds=60)
def challenge_step(challenge_id):
    try:
        user_email = request.user['email']
        result = controller.verify_request_headers(
            user_email,
            challenge_id,
            request.headers
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/complete/<challenge_id>', methods=['POST'])
@require_auth
def complete_challenge(challenge_id):
    try:
        user_email = request.user['email']
        data = request.get_json()
        
        if not data or 'assembled_key' not in data:
            return jsonify({'error': 'Missing assembled_key in request'}), 400
            
        result = controller.complete_challenge(
            user_email,
            challenge_id,
            data['assembled_key']
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500