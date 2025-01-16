from datetime import datetime, timezone
from app.database.db_config import Database
import os
from dotenv import load_dotenv
from typing import List
from ..models.challenge import Challenge

load_dotenv()

class ChallengeController:
    def __init__(self, ):
        self.db = Database()
        self.table = self.db.connect().Table(os.getenv("DYNAMODB_TABLE_NAME"))
        
    def get_challenge(self, challenge_id: str) -> Challenge:
        response = self.table.get_item(Key={"pk": "CHALLENGE", "sk": challenge_id})
        if "Item" not in response:
            return None
        challenge_data = response["Item"]
        return Challenge.from_db(challenge_data).to_dict()
    
    def get_all_challenges(self) -> List[Challenge]:
        response = self.table.query(KeyConditionExpression="pk = :pk", ExpressionAttributeValues={":pk": "CHALLENGE"})
        challenges = []
        for item in response["Items"]:
            challenges.append(Challenge.from_db(item))
        # Return the Challenges to_dict
        return [challenge.to_dict() for challenge in challenges]
    
    def create_challenge(self, data: dict) -> Challenge:
        challenge = Challenge.from_dict(data)
        challenge_item = challenge.to_dict()
        self.table.put_item(Item=challenge_item)
        return challenge.to_dict()
