from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

# PASSWORD HASH
def password_hash(password: str) -> str:
    return pwd_context.hash(password)


def password_verify(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# OTP HASH
def opt_hash(otp: str) -> str:
    return pwd_context.hash(otp)


def otp_verfiy(otp: str, hashed: str) -> str:
    return pwd_context.verify(otp, hashed)