from datetime import datetime, timedelta, timezone
import jwt
def issue_access(secret: str, user_id: str) -> str:
    return jwt.encode({"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=12)}, secret, algorithm="HS256")
def decode_access(secret: str, token: str) -> str:
    return jwt.decode(token, secret, algorithms=["HS256"])["sub"]
