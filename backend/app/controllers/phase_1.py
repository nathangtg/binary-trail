from datetime import datetime, timezone
import uuid
import random
import base64
from typing import Dict, Optional
from app.utils.auth import AuthUtil
from app.database.db_config import Database
import os
from dotenv import load_dotenv
from app.models.user import User

load_dotenv()

class Phase1Controller:
    def __init__(self):
        self.db = Database()
        self.table = self.db.connect().Table(os.getenv("DYNAMODB_TABLE_NAME"))
        
    def _generate_riddles_and_headers(self) -> Dict:
        headers = {
            'X-Quest-Key': str(uuid.uuid4())[:8],
            'X-Quest-Sequence': base64.b64encode(str(random.randint(1000, 9999)).encode()).decode(),
            'X-Quest-Token': str(uuid.uuid4())[:8]
        }
        
        # Create individual riddles for each header with increasing complexity
        riddles = {
            'X-Quest-Key': f"First guardian's key lies in UUID's embrace, eight characters hold the secret space: '{headers['X-Quest-Key']}'",
            'X-Quest-Sequence': f"Second trial awaits, in base64's maze. Decode the number's encrypted haze: '{headers['X-Quest-Sequence']}'",
            'X-Quest-Token': f"Final seal requires a token rare, another UUID fragment fair: '{headers['X-Quest-Token']}'"
        }
        
        return {
            'riddles': riddles,
            'required_headers': headers
        }

    def create_challenge(self, user_email: str) -> Dict:
        """Initialize a new challenge for a user"""
        riddle_data = self._generate_riddles_and_headers()
        challenge_id = str(uuid.uuid4())
        
        # Create challenge entry
        challenge_item = {
            'pk': f"USER#{user_email}",
            'sk': f"CHALLENGE#PHASE1#{challenge_id}",
            'challenge_id': challenge_id,
            'phase': 1,
            'status': 'active',
            'required_headers': riddle_data['required_headers'],
            'solved_headers': [],
            'attempts': 0,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'last_request_time': datetime.now(timezone.utc).isoformat()
        }
        
        self.table.put_item(Item=challenge_item)
        
        # Return first riddle only
        return {
            'challenge_id': challenge_id,
            'current_riddle': riddle_data['riddles']['X-Quest-Key'],
            'message': 'Begin your quest by solving the first guardian\'s riddle.',
            'progress': '0/3 headers solved'
        }

    def verify_request_header(self, user_email: str, challenge_id: str, headers: Dict) -> Dict:
        """Verify a single request header and provide the next riddle"""
        # Get challenge state
        response = self.table.get_item(
            Key={
                'pk': f"USER#{user_email}",
                'sk': f"CHALLENGE#PHASE1#{challenge_id}"
            }
        )
        
        if 'Item' not in response:
            raise ValueError("Challenge not found")
            
        challenge = response['Item']
        
        # Check rate limiting
        last_request = datetime.fromisoformat(challenge['last_request_time'])
        current_time = datetime.now(timezone.utc)
        if (current_time - last_request).seconds < 12:  
            raise ValueError("Rate limit exceeded. Wait a few seconds.")
        
        # Determine which header should be solved next
        header_sequence = ['X-Quest-Key', 'X-Quest-Sequence', 'X-Quest-Token']
        solved_headers = challenge['solved_headers']
        current_header = None
        
        for header in header_sequence:
            if header not in solved_headers:
                current_header = header
                break
                
        if not current_header:
            raise ValueError("All headers already solved")
            
        # Verify the current header
        required_headers = challenge['required_headers']
        if headers.get(current_header) != required_headers[current_header]:
            challenge['attempts'] += 1
            self._update_challenge(challenge)
            raise ValueError(f"Invalid header value. Attempt {challenge['attempts']}")
        
        # Mark header as solved
        challenge['solved_headers'].append(current_header)
        next_header = None
        next_riddle = None
        
        # Get next riddle if there are more headers to solve
        riddle_data = self._generate_riddles_and_headers()
        for header in header_sequence:
            if header not in challenge['solved_headers']:
                next_header = header
                next_riddle = riddle_data['riddles'][header]
                break
        
        self._update_challenge(challenge)
        
        response = {
            'success': True,
            'progress': f"{len(challenge['solved_headers'])}/3 headers solved"
        }
        
        if next_riddle:
            response['message'] = 'Header solved correctly! Here\'s your next riddle.'
            response['next_riddle'] = next_riddle
        else:
            # All headers solved - generate completion key
            completion_key = self._generate_completion_key(challenge['required_headers'])
            response['message'] = 'All headers solved! Now assemble the completion key.'
            response['completion_hint'] = 'Combine the values in order: key + decoded_sequence + token'
        
        return response

    def complete_challenge(self, user_email: str, challenge_id: str, completion_key: str) -> Dict:
        """Verify the completion key and complete the challenge"""
        response = self.table.get_item(
            Key={
                'pk': f"USER#{user_email}",
                'sk': f"CHALLENGE#PHASE1#{challenge_id}"
            }
        )
        
        if 'Item' not in response:
            raise ValueError("Challenge not found")
            
        challenge = response['Item']
        
        if len(challenge['solved_headers']) < 3:
            raise ValueError("Must solve all header riddles first")
            
        correct_key = self._generate_completion_key(challenge['required_headers'])
        
        if completion_key != correct_key:
            challenge['attempts'] += 1
            self._update_challenge(challenge)
            raise ValueError(f"Invalid completion key. Attempt {challenge['attempts']}")
        
        # Mark challenge as completed
        challenge['status'] = 'completed'
        challenge['completed_at'] = datetime.now(timezone.utc).isoformat()
        self._update_challenge(challenge)
        
        # Create Phase 2 access token
        phase2_token = self._generate_phase2_token(user_email)
        
        return {
            'success': True,
            'message': 'Phase 1 completed! Welcome to the Crypto Maze.',
            'phase2_token': phase2_token,
            'next_phase_url': '/phase2/begin'
        }

    def _generate_completion_key(self, headers: Dict) -> str:
        """Generate the final completion key from the headers"""
        decoded_sequence = str(base64.b64decode(headers['X-Quest-Sequence'].encode()).decode())
        return f"{headers['X-Quest-Key']}{decoded_sequence}{headers['X-Quest-Token']}"

    def _update_challenge(self, challenge: Dict) -> None:
        challenge['updated_at'] = datetime.now(timezone.utc).isoformat()
        challenge['last_request_time'] = datetime.now(timezone.utc).isoformat()
        self.table.put_item(Item=challenge)

    def _generate_phase2_token(self, user_email: str) -> str:
        user = User.from_dict(self.table.get_item(Key={"pk": f"USER#{user_email}", "sk": "PROFILE"})["Item"])
        
        if not user:
            raise ValueError("User not found")
        
        return ({           
            "message": "Welcome to Phase 2. Here is your access token.",
            "token": AuthUtil.generate_token(user, expires_in=86400),
            "constraint": "You have 24 hours to complete Phase 2."
        })