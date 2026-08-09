from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def password_hash(password: str) -> str:
    return pwd_context.hash(password)


def password_verify(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
