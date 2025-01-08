from datetime import datetime, timezone
import uuid
import random
import base64
from typing import Dict, List, Optional
from app.utils.auth import AuthUtil
from app.database.db_config import Database
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Logging
import logging
logging.basicConfig(level=logging.INFO)

class Phase2Controller:
    def __init__(self):
        self.db = Database()
        self.table = self.db.connect().Table(os.getenv("DYNAMODB_TABLE_NAME"))
        self.encoding_methods = {
            'base64': self._encode_base64,
            'caesar': self._encode_caesar,
            'xor': self._encode_xor,
            'custom': self._encode_custom
        }
        
    def initialize_maze(self, user_email: str) -> Dict:
        """Create new maze instance with encoded messages"""
        maze_id = str(uuid.uuid4())
        coordinates = self._generate_maze_path()
        encoded_messages = self._create_encoded_messages(coordinates)
        
        maze_item = {
            'pk': f"USER#{user_email}",
            'sk': f"MAZE#{maze_id}",
            'maze_id': maze_id,
            'status': 'active',
            'coordinates': coordinates,
            'current_position': 0,
            'collected_tokens': [],
            'attempts': 0,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        self.table.put_item(Item=maze_item)
        
        return {
            'maze_id': maze_id,
            'first_message': encoded_messages[0],
            'encoding_type': 'base64'
        }

    def verify_solution(self, user_email: str, maze_id: str, decoded_message: str) -> Dict:
        """Verify decoded message and provide next challenge"""
        maze = self._get_maze(user_email, maze_id)
        current_pos = int(maze['current_position'])
        
        if not self._verify_coordinate(maze, current_pos, decoded_message):
            maze['attempts'] += 1
            self._update_maze(maze)
            raise ValueError(f"Invalid solution. Attempt {maze['attempts']}")
            
        # Generate token for correct solution
        token = self._generate_token()
        maze['collected_tokens'].append(token)
        maze['current_position'] += 1
        
        # Check if maze is completed
        if maze['current_position'] >= len(maze['coordinates']):
            maze['status'] = 'completed'
            self._update_maze(maze)
            return {
                'success': True,
                'message': 'Maze completed!',
                'final_tokens': maze['collected_tokens']
            }
            
        # Provide next encoded message
        next_message = self._create_encoded_messages([maze['coordinates'][int(maze['current_position'])]])[0]
        self._update_maze(maze)
        
        return {
            'success': True,
            'token': token,
            'next_message': next_message,
            'encoding_type': self._get_next_encoding_type(maze['current_position'])
        }

    def _verify_coordinate(self, maze: Dict, position: int, decoded_message: str) -> bool:
        x = int(maze['coordinates'][position]['x'])
        y = int(maze['coordinates'][position]['y'])
        expected = f"Navigate to ({x}, {y})"
        return decoded_message.strip() == expected

    def _generate_maze_path(self) -> List[Dict]:
        coordinates = []
        x, y = 0, 0
        for _ in range(4):
            x += random.randint(-2, 2)
            y += random.randint(-2, 2)
            coordinates.append({'x': int(x), 'y': int(y)})
        return coordinates

    def _create_encoded_messages(self, coordinates: List[Dict]) -> List[str]:
        """Create encoded messages for each coordinate"""
        messages = []
        for i, coord in enumerate(coordinates):
            message = f"Navigate to ({coord['x']}, {coord['y']})"
            encoding_type = self._get_next_encoding_type(i)
            messages.append(self.encoding_methods[encoding_type](message))
        return messages

    def _encode_base64(self, message: str) -> str:
        return base64.b64encode(message.encode()).decode()

    def _encode_caesar(self, message: str, shift: int = 3) -> str:
        result = ""
        for char in message:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    def _encode_xor(self, message: str, key: int = 42) -> str:
        return ''.join([chr(ord(c) ^ key) for c in message])

    def _encode_custom(self, message: str) -> str:
        # Custom encoding pattern (reverse + base64)
        return base64.b64encode(message[::-1].encode()).decode()

    def _get_next_encoding_type(self, position: int) -> str:
        types = ['base64', 'caesar', 'xor', 'custom']
        return types[int(position) % len(types)]

    def _generate_token(self) -> str:
        return str(uuid.uuid4())[:8]

    def _get_maze(self, user_email: str, maze_id: str) -> Dict:
        response = self.table.get_item(
            Key={
                'pk': f"USER#{user_email}",
                'sk': f"MAZE#{maze_id}"
            }
        )
        if 'Item' not in response:
            raise ValueError("Maze not found")
        return response['Item']

    def _update_maze(self, maze: Dict) -> None:
        maze['updated_at'] = datetime.now(timezone.utc).isoformat()
        self.table.put_item(Item=maze)
        
    def verify_completion(self, user_email: str, maze_id: str, collected_tokens: str) -> Dict:
        maze = self._get_maze(user_email, maze_id)
        
        # Query DynamoDB using both pk (partition key) and sk (sort key)
        response = self.table.query(
            KeyConditionExpression="pk = :pk and begins_with(sk, :sk)", 
            ExpressionAttributeValues={
                ":pk": f"USER#{user_email}",
                ":sk": f"MAZE#{maze_id}" 
            }
        )
        
        # Get all tokens from the response
        tokens = [item['collected_tokens'] for item in response['Items']]
        collected_tokens_from_db = [token for sublist in tokens for token in sublist]
        collected_tokens_from_request = ''.join(collected_tokens_from_db)
        
        # Compare the tokens
        if collected_tokens_from_request != collected_tokens:
            logging.info(f"Collected tokens from request: {collected_tokens}")
            logging.info(f"Expected tokens: {collected_tokens_from_request}")
            raise ValueError("Invalid token collection")
        
        maze['status'] = 'completed'
        self._update_maze(maze)
        
        return {
            'success': True,
            'message': 'Maze completed!',
            'final_tokens': maze['collected_tokens']
        }
