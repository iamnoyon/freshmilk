from datetime import datetime, timedelta, timezone
import secrets


def generate_otp() -> str:
    return f"{secrets.randbelow(100000):05d}"


def get_otp_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=2)
