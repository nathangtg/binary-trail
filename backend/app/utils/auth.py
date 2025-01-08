import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from ..models.user import User  
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")

class AuthUtil:
    @staticmethod
    def generate_token(user: User, expires_in: int = 3600) -> str:
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
            "iat": datetime.now(timezone.utc),
            "user": user.to_dict(),  
        }
        # Encode the token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header is missing or invalid"}), 401
        
        token = auth_header.split(" ")[1]
        try:
            payload = AuthUtil.decode_token(token)
            user_data = payload.get("user")
            if not user_data:
                raise ValueError("Invalid token payload.")
            
            request.user = User.from_dict(user_data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        
        return func(*args, **kwargs)
    
    return wrapper