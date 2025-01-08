from datetime import datetime, timezone
import uuid
import random
import base64
from typing import Dict, Optional
from app.utils.auth import AuthUtil
from app.database.db_config import Database
import os
from dotenv import load_dotenv

load_dotenv()

class Phase1Controller:
    def __init__(self):
        self.db = Database()
        self.table = self.db.connect().Table(os.getenv("DYNAMODB_TABLE_NAME"))
        
    def _generate_riddle_and_headers(self) -> Dict:
        headers = {
            'X-Quest-Key': str(uuid.uuid4())[:8],
            'X-Quest-Sequence': base64.b64encode(str(random.randint(1000, 9999)).encode()).decode(),
            'X-Quest-Token': str(uuid.uuid4())[:8]
        }
        
        # Create a riddle that encodes these headers
        riddle_templates = [
            f"In the garden of bits, a key blooms: '{headers['X-Quest-Key']}' marks the path.",
            f"Sequence whispers in base64: '{headers['X-Quest-Sequence']}' guides the way.",
            f"A token of trust: '{headers['X-Quest-Token']}' unlocks the gates."
        ]
        
        return {
            'riddle': ' '.join(riddle_templates),
            'required_headers': headers
        }

    def create_challenge(self, user_email: str) -> Dict:
        """Initialize a new challenge for a user"""
        riddle_data = self._generate_riddle_and_headers()
        challenge_id = str(uuid.uuid4())
        
        # Create challenge entry
        challenge_item = {
            'pk': f"USER#{user_email}",
            'sk': f"CHALLENGE#PHASE1#{challenge_id}",
            'challenge_id': challenge_id,
            'phase': 1,
            'status': 'active',
            'required_headers': riddle_data['required_headers'],
            'key_fragments': [],
            'attempts': 0,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'last_request_time': datetime.now(timezone.utc).isoformat()
        }
        
        self.table.put_item(Item=challenge_item)
        
        return {
            'challenge_id': challenge_id,
            'riddle': riddle_data['riddle'],
            'message': 'Decode the riddle to find the required headers for your quest.'
        }

    def verify_request_headers(self, user_email: str, challenge_id: str, headers: Dict) -> Dict:
        """Verify request headers and generate next key fragment"""
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
        if (current_time - last_request).seconds < 12:  # 5 requests per minute max
            raise ValueError("Rate limit exceeded. Wait a few seconds.")
            
        # Verify headers
        required_headers = challenge['required_headers']
        for header, value in required_headers.items():
            if headers.get(header) != value:
                challenge['attempts'] += 1
                self._update_challenge(challenge)
                raise ValueError(f"Invalid headers. Attempt {challenge['attempts']}")
        
        # Generate new key fragment
        key_fragment = self._generate_key_fragment()
        challenge['key_fragments'].append(key_fragment)
        self._update_challenge(challenge)
        
        return {
            'success': True,
            'key_fragment': key_fragment,
            'message': 'Fragment obtained. Combine all fragments in order.'
        }

    def complete_challenge(self, user_email: str, challenge_id: str, assembled_key: str) -> Dict:
        """Verify the assembled key and complete the challenge"""
        response = self.table.get_item(
            Key={
                'pk': f"USER#{user_email}",
                'sk': f"CHALLENGE#PHASE1#{challenge_id}"
            }
        )
        
        if 'Item' not in response:
            raise ValueError("Challenge not found")
            
        challenge = response['Item']
        correct_key = ''.join(challenge['key_fragments'])
        
        if assembled_key != correct_key:
            challenge['attempts'] += 1
            self._update_challenge(challenge)
            raise ValueError(f"Invalid key. Attempt {challenge['attempts']}")
        
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

    def _generate_key_fragment(self) -> str:
        return str(uuid.uuid4())[:8]

    def _update_challenge(self, challenge: Dict) -> None:
        challenge['updated_at'] = datetime.now(timezone.utc).isoformat()
        challenge['last_request_time'] = datetime.now(timezone.utc).isoformat()
        self.table.put_item(Item=challenge)

    def _generate_phase2_token(self, user_email: str) -> str:
        return AuthUtil.generate_token({
            'email': user_email,
            'phase': 2,
            'exp': datetime.now(timezone.utc) + datetime.timedelta(hours=1)
        })