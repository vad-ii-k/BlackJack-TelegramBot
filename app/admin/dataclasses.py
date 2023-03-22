from dataclasses import dataclass, field
from hashlib import sha256
from typing import Optional

from aiohttp_session import Session


@dataclass
class Admin:
    id: int = field(default_factory=int)
    email: str = field(default_factory=int)
    password: str | None = None

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Session) -> Optional["Admin"]:
        return cls(
            id=session["admin_data"]["id"], email=session["admin_data"]["email"]
        )
