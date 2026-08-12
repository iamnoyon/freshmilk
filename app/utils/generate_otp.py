import os
import secrets
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

def generate_otp() -> str:
    return f"{secrets.randbelow(100000):05d}"


def get_otp_expiry() -> datetime:
    expire_withIn = os.getenv('SMS_EXPIRE_TIME')
    
    return datetime.now(timezone.utc) + timedelta(minutes=expire_withIn)


def generate_password() -> str:
    return f"{secrets.randbelow(100000):04d}"
