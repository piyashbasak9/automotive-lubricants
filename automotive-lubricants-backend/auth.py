from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
import importlib
import importlib.util

# Load dotenv dynamically to avoid static import errors in environments
# where python-dotenv isn't installed.
if importlib.util.find_spec("dotenv"):
    load_dotenv = importlib.import_module("dotenv").load_dotenv
    load_dotenv()
else:
    def load_dotenv():
        return None

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)