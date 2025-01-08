from functools import wraps
from flask import request, jsonify
from datetime import datetime, timezone, timedelta
import os
from ..database.db_config import Database
import time
from typing import Optional

class RateLimitExceeded(Exception):
    pass

class RateLimit:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.db = Database()
        self.table = self.db.connect().Table(os.getenv("DYNAMODB_TABLE_NAME"))
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def _get_rate_limit_key(self, user_email: str) -> dict:
        return {
            "pk": f"USER#{user_email}",
            "sk": f"RATELIMIT#API"
        }

    def _clean_old_requests(self, requests: list) -> list:
        cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=self.window_seconds)
        return [req for req in requests if datetime.fromisoformat(req) > cutoff_time]

    def check_rate_limit(self, user_email: str) -> bool:
        try:
            # Get current rate limit record
            response = self.table.get_item(
                Key=self._get_rate_limit_key(user_email)
            )

            current_time = datetime.now(timezone.utc)
            
            if 'Item' in response:
                # Clean and check existing requests
                requests = self._clean_old_requests(response['Item'].get('requests', []))
                
                if len(requests) >= self.max_requests:
                    return False
                
                # Add new request timestamp
                requests.append(current_time.isoformat())
                
                # Update rate limit record
                self.table.update_item(
                    Key=self._get_rate_limit_key(user_email),
                    UpdateExpression="SET requests = :r, updated_at = :u",
                    ExpressionAttributeValues={
                        ':r': requests,
                        ':u': current_time.isoformat()
                    }
                )
            else:
                # Create new rate limit record
                self.table.put_item(
                    Item={
                        **self._get_rate_limit_key(user_email),
                        'requests': [current_time.isoformat()],
                        'created_at': current_time.isoformat(),
                        'updated_at': current_time.isoformat()
                    }
                )
            
            return True

        except Exception as e:
            # Log the error in production
            print(f"Rate limit check error: {str(e)}")
            # On error, allow the request to proceed
            return True

    def get_remaining_requests(self, user_email: str) -> dict:
        """Get remaining requests and reset time for the user"""
        try:
            response = self.table.get_item(
                Key=self._get_rate_limit_key(user_email)
            )
            
            if 'Item' in response:
                requests = self._clean_old_requests(response['Item'].get('requests', []))
                remaining = max(0, self.max_requests - len(requests))
                
                if requests:
                    oldest_request = datetime.fromisoformat(requests[0])
                    reset_time = oldest_request + timedelta(seconds=self.window_seconds)
                else:
                    reset_time = datetime.now(timezone.utc)
                
                return {
                    'remaining': remaining,
                    'reset': reset_time.isoformat()
                }
            
            return {
                'remaining': self.max_requests,
                'reset': datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:
            # Log the error in production
            print(f"Get remaining requests error: {str(e)}")
            return {
                'remaining': self.max_requests,
                'reset': datetime.now(timezone.utc).isoformat()
            }


def rate_limit(max_requests: int = 5, window_seconds: int = 60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.user or not hasattr(request.user, 'email'):
                return jsonify({'error': 'Unauthorized'}), 401
                
            rate_limiter = RateLimit(max_requests, window_seconds)
            user_email = request.user.email
            
            if not rate_limiter.check_rate_limit(user_email):
                remaining = rate_limiter.get_remaining_requests(user_email)
                
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'remaining_requests': remaining['remaining'],
                    'reset_time': remaining['reset']
                })
                
                response.headers['X-RateLimit-Remaining'] = str(remaining['remaining'])
                response.headers['X-RateLimit-Reset'] = remaining['reset']
                return response, 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator