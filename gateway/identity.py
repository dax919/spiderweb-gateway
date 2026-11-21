"""Verify who is calling the gateway, based on a signed JWT."""
import os
from dataclasses import dataclass

import jwt
from fastapi import Header, HTTPException

from gateway.events import log_event

JWT_SECRET = os.getenv("GATEWAY_JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"


@dataclass(frozen=True)
class Employee:
    employee_id: str
    role: str


def get_employee(authorization: str = Header(default="")) -> Employee:
    """Turn the Bearer token into an Employee, or reject the request."""
    token = authorization.removeprefix("Bearer ").strip()
    try:
        claims = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "role", "exp"]},
        )
    except jwt.PyJWTError as error:
        log_event("auth_failed", reason=type(error).__name__)
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return Employee(employee_id=claims["sub"], role=claims["role"])