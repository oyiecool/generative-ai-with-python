# src/aikit/security.py
import time
from collections import defaultdict, deque
from dataclasses import dataclass

import jwt                                    # uv add pyjwt[crypto]
from fastapi import Depends, Header, HTTPException

from aikit.settings import get_settings


@dataclass
class User:
    id: str
    groups: list[str]


_jwks = jwt.PyJWKClient(get_settings().oidc_jwks_url)


def authenticate(authorization: str = Header(...)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    token = authorization.removeprefix("Bearer ")
    try:
        key = _jwks.get_signing_key_from_jwt(token).key
        claims = jwt.decode(token, key, algorithms=["RS256"],
                            audience=get_settings().oidc_audience)
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid token")
    return User(id=claims["sub"], groups=claims.get("groups", []))


_windows: dict[str, deque] = defaultdict(deque)


def rate_limit(user: User = Depends(authenticate), per_minute: int = 20):
    now, q = time.time(), _windows[user.id]
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= per_minute:
        raise HTTPException(429, "rate limit exceeded", headers={"Retry-After": "30"})
    q.append(now)
