from datetime import datetime, timezone
import uuid
import random
import base64
from typing import Dict, Optional, List, Tuple
from app.utils.auth import AuthUtil
from app.database.db_config import Database
import os
from dotenv import load_dotenv
from app.models.user import User
from datetime import timedelta

load_dotenv()

class Phase1Controller:
    def __init__(self):
        self.db = Database()
        self.table = self.db.connect().Table(os.getenv("DYNAMODB_TABLE_NAME"))
        self.header_sequence = ['X-Quest-Key', 'X-Quest-Sequence', 'X-Quest-Token']
        
    def _generate_riddles_and_headers(self, existing_headers: Dict = None) -> Dict:
        if existing_headers is None:
            sequence_number = str(random.randint(1000, 9999))
            encoded_sequence = base64.b64encode(sequence_number.encode()).decode('utf-8')
            
            headers = {
                'X-Quest-Key': str(uuid.uuid4())[:8],
                'X-Quest-Sequence': sequence_number,
                'X-Quest-Sequence-Encoded': encoded_sequence,
                'X-Quest-Token': str(uuid.uuid4())[:8]
            }
        else:
            # Use existing header values
            headers = existing_headers

        # Create riddles using the header values
        riddles = {
            'X-Quest-Key': {
                'text': f"First guardian's key lies in UUID's embrace, eight characters hold the secret space: '{headers['X-Quest-Key']}'",
                'hint': "Copy the exact eight characters shown in the riddle",
                'order': 1
            },
            'X-Quest-Sequence': {
                'text': f"Second trial awaits, in base64's maze. Decode this value to proceed: '{headers['X-Quest-Sequence-Encoded']}'",
                'hint': "Submit the decoded number (should be between 1000-9999)",
                'order': 2
            },
            'X-Quest-Token': {
                'text': f"Final seal requires a token rare, another UUID fragment fair: '{headers['X-Quest-Token']}'",
                'hint': "Copy the exact eight characters shown in the riddle",
                'order': 3
            }
        }
        
        return {
            'riddles': riddles,
            'required_headers': headers
        }

    def _validate_challenge_state(self, challenge: Dict, expected_header: str) -> None:
        """Validate the challenge state and header sequence"""
        solved_headers = challenge.get('solved_headers', [])
        current_index = len(solved_headers)
        
        if current_index >= len(self.header_sequence):
            raise ValueError("All headers already solved")
            
        expected_header_in_sequence = self.header_sequence[current_index]
        if expected_header != expected_header_in_sequence:
            raise ValueError(f"Invalid header sequence. Expected {expected_header_in_sequence}, got {expected_header}")

    def create_challenge(self, user_email: str) -> Dict:
        """Initialize a new challenge for a user"""
        # Check if user has any active challenges
        existing_challenges = self.table.query(
            KeyConditionExpression="pk = :pk AND begins_with(sk, :sk)",
            ExpressionAttributeValues={
                ":pk": f"USER#{user_email}",
                ":sk": "CHALLENGE#PHASE1#"
            }
        ).get('Items', [])
        
        active_challenges = [c for c in existing_challenges if c['status'] == 'active']
        if active_challenges:
            raise ValueError("You already have an active Phase 1 challenge")

        riddle_data = self._generate_riddles_and_headers()
        challenge_id = str(uuid.uuid4())
        
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
            'last_request_time': datetime.now(timezone.utc).isoformat(),
            'expiry_time': (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        }
        
        self.table.put_item(Item=challenge_item)
        
        first_riddle = riddle_data['riddles']['X-Quest-Key']
        return {
            'challenge_id': challenge_id,
            'current_riddle': first_riddle['text'],
            'hint': first_riddle['hint'],
            'message': 'Begin your quest by solving the first guardian\'s riddle.',
            'progress': '0/3 headers solved',
            'expires_in': '24 hours'
        }

    def verify_request_header(self, user_email: str, challenge_id: str, headers: Dict) -> Dict:
        """Verify a single request header and provide the next riddle"""
        response = self.table.get_item(
            Key={
                'pk': f"USER#{user_email}",
                'sk': f"CHALLENGE#PHASE1#{challenge_id}"
            }
        )
        
        if 'Item' not in response:
            raise ValueError("Challenge not found")
            
        challenge = response['Item']
        
        # Check challenge expiry
        if datetime.fromisoformat(challenge['expiry_time']) < datetime.now(timezone.utc):
            raise ValueError("Challenge has expired. Please start a new challenge.")
            
        if challenge['status'] != 'active':
            raise ValueError("Challenge is not active")

        # Check rate limiting
        last_request = datetime.fromisoformat(challenge['last_request_time'])
        current_time = datetime.now(timezone.utc)
        if (current_time - last_request).seconds < 12:  
            raise ValueError("Rate limit exceeded. Please wait 12 seconds between attempts.")
        
        # Determine which header should be solved next
        solved_headers = challenge.get('solved_headers', [])
        if len(solved_headers) >= len(self.header_sequence):
            raise ValueError("All headers already solved")
            
        current_header = self.header_sequence[len(solved_headers)]
        
        # Validate header presence
        if current_header not in headers:
            raise ValueError(f"Missing required header: {current_header}")
            
        # Verify the current header
        required_headers = challenge['required_headers']
        submitted_value = headers[current_header]
        
        # Validate header value
        if current_header == 'X-Quest-Sequence':
            expected_value = required_headers[current_header]
            if submitted_value != expected_value:
                challenge['attempts'] = challenge.get('attempts', 0) + 1
                self._update_challenge(challenge)
                raise ValueError(f"Invalid sequence number. Expected the decoded value. Attempt {challenge['attempts']}")
        else:
            expected_value = required_headers[current_header]
            if submitted_value != expected_value:
                challenge['attempts'] = challenge.get('attempts', 0) + 1
                self._update_challenge(challenge)
                raise ValueError(f"Invalid {current_header} value. Attempt {challenge['attempts']}")
        
        # Mark header as solved
        challenge['solved_headers'] = solved_headers + [current_header]
        
        # Get next riddle if available
        riddle_data = self._generate_riddles_and_headers(challenge['required_headers'])
        response = {
            'success': True,
            'progress': f"{len(challenge['solved_headers'])}/3 headers solved"
        }
        
        if len(challenge['solved_headers']) < len(self.header_sequence):
            next_header = self.header_sequence[len(challenge['solved_headers'])]
            next_riddle = riddle_data['riddles'][next_header]
            response.update({
                'message': f'Header solved correctly! Moving to step {len(challenge["solved_headers"]) + 1}.',
                'next_riddle': next_riddle['text'],
                'hint': next_riddle['hint']
            })
        else:
            completion_key = self._generate_completion_key(challenge['required_headers'])
            response.update({
                'message': 'All headers solved! Now assemble the completion key.',
                'completion_hint': 'Combine the values in this order: key + sequence + token\nExample: abc123 + 4567 + def890 = abc1234567def890'
            })
        
        self._update_challenge(challenge)
        return response

    def _generate_completion_key(self, headers: Dict) -> str:
        """Generate completion key using stored decoded sequence value"""
        return f"{headers['X-Quest-Key']}{headers['X-Quest-Sequence']}{headers['X-Quest-Token']}"

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
        
        # Verify challenge state
        if challenge['status'] != 'active':
            raise ValueError("Challenge is not active")
            
        if datetime.fromisoformat(challenge['expiry_time']) < datetime.now(timezone.utc):
            raise ValueError("Challenge has expired. Please start a new challenge.")
            
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
        
        # Generate Phase 2 access token
        phase2_token = self._generate_phase2_token(user_email)
        
        return {
            'success': True,
            'message': 'Congratulations! Phase 1 completed successfully.',
            'stats': {
                'attempts': challenge['attempts'],
                'time_taken': (datetime.fromisoformat(challenge['completed_at']) - 
                             datetime.fromisoformat(challenge['created_at'])).total_seconds() / 60,
                'completion_date': challenge['completed_at']
            },
            'phase2_token': phase2_token,
            'next_phase_url': '/phase2/begin'
        }

    def _update_challenge(self, challenge: Dict) -> None:
        """Update challenge in database with timestamps"""
        challenge['updated_at'] = datetime.now(timezone.utc).isoformat()
        challenge['last_request_time'] = datetime.now(timezone.utc).isoformat()
        self.table.put_item(Item=challenge)

    def _generate_phase2_token(self, user_email: str) -> Dict:
        """Generate access token for Phase 2"""
        user = User.from_dict(self.table.get_item(
            Key={"pk": f"USER#{user_email}", "sk": "PROFILE"})["Item"])
        
        if not user:
            raise ValueError("User not found")
        
        return {           
            "message": "Welcome to Phase 2. Your access token is ready.",
            "token": AuthUtil.generate_token(user, expires_in=86400),
            "expires_in": "24 hours",
            "instructions": "Use this token in the Authorization header for all Phase 2 requests."
        }