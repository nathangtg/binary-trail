from datetime import datetime, timezone
import uuid
import random
import base64
from typing import Dict, List, Optional, Tuple
from app.utils.auth import AuthUtil
from app.database.db_config import Database
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Logging
import logging
logging.basicConfig(level=logging.INFO)

class Phase2Controller:
    """
    Controller for Phase 2 of the Invincible Maze game.
    This phase challenges players with various encryption puzzles they must solve
    to progress through the maze.
    """

    ENCRYPTION_KEYS = {
        'caesar': 3,  # Shift by 3 positions
        'xor': 42,    # XOR with key 42
    }

    ENCRYPTION_HINTS = {
        'base64': "This message is encoded in Base64. Use a Base64 decoder to reveal the coordinates.",
        'caesar': "This is a Caesar cipher with a shift of 3. Shift each letter back by 3 positions (A->X, B->Y, etc).",
        'xor': "This message is XOR encoded with the key 42. Apply XOR(42) to each character.",
        'custom': "This message is reversed and then Base64 encoded. First decode from Base64, then reverse the result."
    }

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
        """
        Create a new maze instance with encoded messages.
        
        Returns:
        Dict containing:
            - maze_id: Unique identifier for this maze instance
            - first_message: The first encoded message to solve
            - encoding_type: Type of encoding used for the first message
            - hint: A helpful hint about how to decode the message
            - total_stages: Total number of stages in the maze
        """
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
            'created_at': datetime.now(timezone.utc).isoformat(),
            'total_stages': len(coordinates)
        }
        
        self.table.put_item(Item=maze_item)
        
        return {
            'maze_id': maze_id,
            'first_message': encoded_messages[0],
            'encoding_type': 'base64',
            'hint': self.ENCRYPTION_HINTS['base64'],
            'total_stages': len(coordinates),
            'current_stage': 1
        }

    def verify_solution(self, user_email: str, maze_id: str, decoded_message: str) -> Dict:
        maze = self._get_maze(user_email, maze_id)
        current_pos = int(maze['current_position'])
        
        if not self._verify_coordinate(maze, current_pos, decoded_message):
            maze['attempts'] += 1
            self._update_maze(maze)
            expected_format = "Navigate to (X, Y) - where X and Y are numbers"
            raise ValueError(
                f"Invalid solution (Attempt {maze['attempts']}).\n"
                f"Expected format: {expected_format}\n"
                f"Make sure your decoding is correct and the message matches exactly."
            )
            
        token = self._generate_token()
        maze['collected_tokens'].append(token)
        maze['current_position'] += 1
        
        if maze['current_position'] >= len(maze['coordinates']):
            maze['status'] = 'completed'
            self._update_maze(maze)
            return {
                'success': True,
                'message': 'Congratulations! You\'ve completed the maze!',
                'final_tokens': maze['collected_tokens'],
                'total_stages': len(maze['coordinates']),
                'current_stage': len(maze['coordinates'])
            }
            
        next_encoding_type = self._get_next_encoding_type(maze['current_position'])
        coords = maze['coordinates'][int(maze['current_position'])]
        message = f"Navigate to ({coords['x']}, {coords['y']})"
        
        # Apply correct encoding based on type
        if next_encoding_type == 'caesar':
            next_message = self._encode_caesar(message)
        elif next_encoding_type == 'base64':
            next_message = self._encode_base64(message)
        elif next_encoding_type == 'xor':
            next_message = self._encode_xor(message)
        else:  # custom
            next_message = self._encode_custom(message)
        
        self._update_maze(maze)
        
        return {
            'success': True,
            'token': token,
            'next_message': next_message,
            'encoding_type': next_encoding_type,
            'hint': self.ENCRYPTION_HINTS[next_encoding_type],
            'current_stage': maze['current_position'] + 1,
            'total_stages': len(maze['coordinates'])
        }

    def _verify_coordinate(self, maze: Dict, position: int, decoded_message: str) -> bool:
        """Verify if the decoded message matches the expected coordinate."""
        x = int(maze['coordinates'][position]['x'])
        y = int(maze['coordinates'][position]['y'])
        expected = f"Navigate to ({x}, {y})"
        return decoded_message.strip() == expected

    def _generate_maze_path(self) -> List[Dict]:
        """Generate a sequence of coordinates forming the maze path."""
        coordinates = []
        x, y = 0, 0
        for _ in range(4):  # 4 stages in total
            x += random.randint(-2, 2)
            y += random.randint(-2, 2)
            coordinates.append({'x': int(x), 'y': int(y)})
        return coordinates

    def _create_encoded_messages(self, coordinates: List[Dict]) -> List[str]:
        """Create encoded messages for each coordinate using different encryption methods."""
        messages = []
        for i, coord in enumerate(coordinates):
            message = f"Navigate to ({coord['x']}, {coord['y']})"
            encoding_type = self._get_next_encoding_type(i)
            messages.append(self.encoding_methods[encoding_type](message))
        return messages

    def _encode_base64(self, message: str) -> str:
        """Encode message using Base64 encoding."""
        return base64.b64encode(message.encode()).decode()

    def _encode_caesar(self, message: str) -> str:
        """Encode message using Caesar cipher with shift of 3, including numbers."""
        shift = self.ENCRYPTION_KEYS['caesar']
        result = ""
        for char in message:
            if char.isalpha():
                is_upper = char.isupper()
                char_code = ord(char.lower()) - ord('a')
                shifted_code = (char_code + shift) % 26
                shifted_char = chr(shifted_code + ord('a'))
                result += shifted_char.upper() if is_upper else shifted_char
            elif char.isdigit():
                # Shift numbers by 3 positions (0-9)
                digit = int(char)
                shifted_digit = (digit + shift) % 10
                result += str(shifted_digit)
            else:
                result += char
        return result

    def _encode_xor(self, message: str) -> str:
        """Encode message using XOR with key 42."""
        key = self.ENCRYPTION_KEYS['xor']
        return ''.join([chr(ord(c) ^ key) for c in message])

    def _encode_custom(self, message: str) -> str:
        """Encode message by reversing it and then applying Base64 encoding."""
        return base64.b64encode(message[::-1].encode()).decode()

    def _get_next_encoding_type(self, position: int) -> str:
        """Get the encryption type for the next message."""
        types = ['base64', 'caesar', 'xor', 'custom']
        return types[int(position) % len(types)]

    def _generate_token(self) -> str:
        """Generate a reward token."""
        return str(uuid.uuid4())[:8]

    def _get_maze(self, user_email: str, maze_id: str) -> Dict:
        """Retrieve maze data from database."""
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
        """Update maze state in database."""
        maze['updated_at'] = datetime.now(timezone.utc).isoformat()
        self.table.put_item(Item=maze)
        
    def get_progress(self, user_email: str, maze_id: str) -> Dict:
        """
        Get current progress information for a maze.
        
        Returns:
        Dict containing:
            - current_stage: Current stage number
            - total_stages: Total number of stages
            - attempts: Number of attempts made
            - status: Current maze status
        """
        maze = self._get_maze(user_email, maze_id)
        return {
            'current_stage': maze['current_position'] + 1,
            'total_stages': len(maze['coordinates']),
            'attempts': maze['attempts'],
            'status': maze['status']
        }