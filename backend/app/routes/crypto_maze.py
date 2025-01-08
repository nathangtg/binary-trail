from flask import Blueprint, request, jsonify
from ..controllers.phase_2 import Phase2Controller
from ..utils.auth import require_auth
from ..utils.rate_limit import rate_limit

bp = Blueprint('phase2', __name__, url_prefix='/phase2')
controller = Phase2Controller()

# Configure Logging
import logging
logging.basicConfig(level=logging.INFO)

@bp.route('/begin', methods=['GET'])
@require_auth
def begin_maze():
    try:
        user_email = request.user.email
        result = controller.initialize_maze(user_email)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/solve/<maze_id>', methods=['POST'])
@require_auth
@rate_limit(max_requests=5, window_seconds=60)
def solve_maze_step(maze_id):
    try:
        user_email = request.user.email
        data = request.get_json()
        
        if not data or 'decoded_message' not in data:
            return jsonify({'error': 'Missing decoded_message in request'}), 400
            
        result = controller.verify_solution(
            user_email,
            maze_id,
            data['decoded_message']
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/complete/<maze_id>', methods=['POST'])
@require_auth
def complete_maze(maze_id):
    try:
        user_email = request.user.email
        data = request.get_json()
        
        if not data or 'collected_tokens' not in data:
            return jsonify({'error': 'Missing collected_tokens in request'}), 400
            
        result = controller.verify_completion(
            user_email,
            maze_id,
            data['collected_tokens']
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500