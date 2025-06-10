import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("SECRET_KEY", "default_secret")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 60 * 60 * 24  # 24시간

def generate_jwt(payload: dict) -> str:
    payload_copy = payload.copy()
    payload_copy["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    return jwt.encode(payload_copy, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def encode_jwt(user):
    payload = {
        "user_id": str(user.email),   # ← 기존: user.id
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    return token
