from app.modules.otp.model import OTP
from app.utils.generate_otp import generate_otp, get_otp_expiry
from app.utils.hash_password import opt_hash

def create_new_otp(phone):
    otp = generate_otp()
    hash_otp = opt_hash(otp)
    expire = get_otp_expiry()
    
    new_otp = OTP(
        phone=phone,
        otp_hash=hash_otp,
        is_verified=False,
        expire_at=expire
    )
    return {new_otp, otp}