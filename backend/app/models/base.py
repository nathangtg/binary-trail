from datetime import datetime
from typing import Dict, Any

class BaseEntity:
    def __init__(self, pk: str, sk: str, created_at: str, updated_at: str):
        self.pk = pk
        self.sk = sk
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            'pk': self.pk,
            'sk': self.sk,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEntity":
        try:
            return cls(
                pk=data['pk'],
                sk=data['sk'],
                created_at=data.get('created_at', datetime.utcnow().isoformat()),
                updated_at=data.get('updated_at', datetime.utcnow().isoformat())
            )
        except KeyError as e:
            raise ValueError(f"Missing required key: {e}")

    @classmethod
    def create(cls, pk: str, sk: str) -> "BaseEntity":
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        return cls(
            pk=pk,
            sk=sk,
            created_at=now,
            updated_at=now
        )

    def update(self) -> None:
        self.updated_at = datetime.utcnow().replace(microsecond=0).isoformat()
