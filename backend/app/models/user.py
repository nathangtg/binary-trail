from .base import BaseEntity
from typing import Optional, Dict
from datetime import datetime, timezone
import bcrypt
import logging


class User(BaseEntity):
    def __init__(
        self,
        pk: str,
        sk: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ):
        created_at = created_at or datetime.now(timezone.utc)
        updated_at = updated_at or datetime.now(timezone.utc)
        super().__init__(pk, sk, created_at, updated_at)

        # Validate email format
        if email and "@" not in email:
            raise ValueError("Invalid email address")

        self.email = email
        self.password = password

        # Hash password if it isn't already hashed
        if password and not password.startswith("$2b$"):
            self.password = self.hash_password(password)

    def hash_password(self, password: str) -> str:
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        salt = bcrypt.gensalt(12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, password: str) -> bool:
        if not self.password:
            raise ValueError("Password not set for this user")

        stored_hash = self.password
        input_bytes = password.encode("utf-8")
        hash_bytes = stored_hash.encode("utf-8")

        try:
            return bcrypt.checkpw(input_bytes, hash_bytes)
        except Exception as e:
            logging.error(f"Password verification error: {str(e)}")
            return False

    def to_dict(self) -> Dict[str, Optional[str]]:
        base_dict = super().to_dict()
        base_dict.update({
            "email": self.email,
            "password": self.password, 
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Optional[str]]) -> "User":
        created_at = (
            datetime.fromisoformat(data["created_at"])
            if data.get("created_at")
            else datetime.now(timezone.utc)
        )
        updated_at = (
            datetime.fromisoformat(data["updated_at"])
            if data.get("updated_at")
            else datetime.now(timezone.utc)
        )

        return cls(
            pk=data["pk"],
            sk=data["sk"],
            created_at=created_at,
            updated_at=updated_at,
            email=data.get("email"),
            password=data.get("password"),
        )

    def update_updated_at(self) -> None:
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"User(pk={self.pk}, sk={self.sk}, "
            f"email={self.email}, created_at={self.created_at}, updated_at={self.updated_at})"
        )
