from datetime import datetime
from typing import Any, Dict, Optional

from ..database import queries
from ..passwords import hash_password
from ..tables import users
from ..utils.strings import slugify
from .email import get_email_hash, normalize_email


async def create_user(
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None
) -> Dict[str, Any]:
    password_hash = None
    if password:
        password_hash = await hash_password(password)

    data: Dict[str, Any] = {
        "name": name,
        "slug": slugify(name),
        "email": normalize_email(email),
        "email_hash": get_email_hash(email),
        "password": password_hash,
        "is_moderator": is_moderator,
        "is_admin": is_admin,
        "joined_at": joined_at or datetime.now(),
    }

    data["id"] = await queries.insert(users, **data)

    return data
