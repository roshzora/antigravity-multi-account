"""
Data models and typed structures for Antigravity Multi-Account Manager.
"""

from dataclasses import dataclass, field
import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class TokenStatus(str, Enum):
    ACTIVE_AUTO_REFRESH = "Active (Auto-refresh)"
    ACTIVE = "Active"
    EXPIRED = "Expired"
    MISSING = "Needs Login"
    ERROR = "Error"


@dataclass
class TokenMetadata:
    email: str
    status: TokenStatus
    expiry_str: Optional[str] = None
    expiry_dt: Optional[datetime.datetime] = None
    has_refresh: bool = False
    auth_method: str = "consumer"
    sub: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return self.status in (TokenStatus.ACTIVE_AUTO_REFRESH, TokenStatus.ACTIVE)


@dataclass
class AccountProfile:
    name: str
    email: str
    path: Path
    created_at: Optional[str] = None
    last_used: Optional[str] = None
    is_active: bool = False
    token_meta: Optional[TokenMetadata] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "path": str(self.path),
            "created_at": self.created_at,
            "last_used": self.last_used,
        }


@dataclass
class HealthCheckItem:
    name: str
    passed: bool
    status: str
    details: str
