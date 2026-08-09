from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.user.model import User
from app.modules.otp.model import OTP

from app.utils.hash_password import password_hash, password_verify
from app.utils.generate_otp import generate_otp, get_otp_expiry
from app.rabbitmq.producer import publish_message


def user_registration(req, db: Session):

    user = db.query(User).filter(User.phone == req.phone).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this phone."
        )

    try:
        hash_pass = password_hash(req.password)

        new_user = User(
            name=req.name,
            nid=req.nid,
            nid_verified=False,
            phone=req.phone,
            password=hash_pass,
            area=req.area,
            road=req.road,
            house=req.house,
            flat=req.flat
        )

        db.add(new_user)
        db.flush()
        db.refresh(new_user)

        otp = generate_otp()
        hash_otp = password_hash(otp)
        expire = get_otp_expiry()

        new_otp = OTP(
            phone=new_user.phone,
            otp_hash=hash_otp,
            is_verified=False,
            expire_at=expire
        )

        db.add(new_otp)
        db.flush()

        payload = {
            "phone": new_user.phone,
            "message": f"Your Milkfresh OTP is: {otp}"
        }

        publish_message(payload)

        db.commit()
        db.refresh(new_otp)

        return {
            "success": True,
            "status_code": status.HTTP_201_CREATED,
            "message": "User is created successfully!"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user."
        )


def verify_otp(req, db: Session):
    otp_record = (
        db.query(OTP)
        .filter(OTP.phone == req.phone, OTP.is_verified == False)
        .order_by(OTP.id.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending OTP found for this phone."
        )

    if otp_record.expire_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="OTP has expired."
        )

    if not password_verify(req.otp, otp_record.otp_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP."
        )

    otp_record.is_verified = True
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "OTP verified successfully!"
    }


def resend_otp(req, db: Session):
    user = db.query(User).filter(User.phone == req.phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found with this phone.'
        )

    otp = generate_otp()
    hash_otp = password_hash(otp)
    expire = get_otp_expiry()

    new_otp = OTP(
        phone=user.phone,
        otp_hash=hash_otp,
        is_verified=False,
        expire_at=expire
    )

    db.add(new_otp)
    db.flush()
    
    payload = {
        "phone": user.phone,
        "message": f"Your Milkfresh OTP is: {otp}"
    }
    
    publish_message(payload)
    
    db.commit()
    db.refresh(new_otp)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": "OTP sent to your phone."
    }