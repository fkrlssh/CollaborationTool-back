import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())
