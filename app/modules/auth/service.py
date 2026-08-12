import traceback
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import defer, Session

from app.modules.user.model import User
from app.modules.otp.model import OTP

from app.utils.token import create_token
from app.utils.hash_password import (
    password_hash, 
    password_verify,
    opt_hash
)
from app.utils.generate_otp import (
    generate_otp, 
    get_otp_expiry, 
    generate_password
)
from app.rabbitmq.producer import publish_message
from app.modules.user.model import ROLE


def user_registration(req, db: Session):

    user = db.query(User).filter(User.phone == req.phone).first()

    if user:
        if not user.phone_verified:
            return {
                "success": True,
                "status_code": 00,
                "message": "OTP sent to your phone"
            }
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this phone."
        )
    

    try:
        new_user = User(
            name=req.name,
            nid=req.nid,
            phone_verified=False,
            phone=req.phone,
            role = ROLE.CUSTOMER,
            area=req.area,
            road=req.road,
            house=req.house,
            flat=req.flat
        )

        db.add(new_user)
        db.flush()
        db.refresh(new_user)

        

        otp = generate_otp()
        hash_otp = opt_hash(otp)
        expire = get_otp_expiry()

        new_otp = OTP(
            phone=new_user.phone,
            otp_hash=hash_otp,
            is_verified=False,
            expire_at=expire
        )

        db.add(new_otp)
        db.flush()

        db.commit()
        db.refresh(new_otp)

        try:
            payload = {
                "phone": new_user.phone,
                "message": f"Your Milkfresh OTP is: {otp}"
            }
            publish_message(payload)
        except Exception:
            pass

        return {
            "success": True,
            "status_code": status.HTTP_201_CREATED,
            "message": "User is created successfully!"
        }

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
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

    is_match_otp = password_verify(req.otp, otp_record.otp_hash)

    if not is_match_otp:
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
    
    db.commit()
    db.refresh(new_otp)

    try:
        payload = {
            "phone": user.phone,
            "message": f"Your Milkfresh OTP is: {otp}"
        }
        publish_message(payload)
    except Exception:
        pass

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": "OTP sent to your phone."
    }


def user_login(req, res, db: Session):
    user = db.query(User).filter(User.phone == req.phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found!'
        )

    is_match_password = password_verify(req.password, user.password)

    if not is_match_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Password is incorrect!'
        )
    verified_otp = db.query(OTP).filter(OTP.phone == req.phoe).where(OTP.is_verified == True).first()

    if not verified_otp:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Please verify you phone number'
        )

    token = create_token(str(user.id), user.phone, user.role, user.permissions)

    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # True in production with HTTPS
        samesite="lax",
        max_age=2592000, # 30 days
    )

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": 'User loggedIn successfull.',
        "token": token
    }


def user_logout(res, current_user):

    res.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=True,
    )

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": 'User loggedout successfull!'
    }


def get_user_profile(current_user, db: Session):
    id = current_user['id']
    user = db.query(User).options(defer(User.password)).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthenticated'
        )
    
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": 'User information retrive successfully!',
        "data": user
    }


def user_password_forgot(req, db: Session):
    user = db.query(User).filter(User.phone == req.phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found with this number'
        )

    password = generate_password()
    hash_pass = password_hash(password)

    # update password
    user.password = hash_pass

    db.commit()
    db.refresh(user)

    try:
        payload = {
            "phone": user.phone,
            "message": f"Your Milkfresh New Password is: {password}"
        }
        publish_message(payload)
    except Exception:
        pass

