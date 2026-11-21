"""Create a signed test token for an employee (development only)."""
import os
import sys
from datetime import datetime, timedelta, timezone

import jwt

SECRET = os.getenv("GATEWAY_JWT_SECRET", "dev-secret-change-me")

employee_id = sys.argv[1] if len(sys.argv) > 1 else "dren"
role = sys.argv[2] if len(sys.argv) > 2 else "backoffice"

token = jwt.encode(
    {
        "sub": employee_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    },
    SECRET,
    algorithm="HS256",
)
print(token)