from fastapi import APIRouter, Depends, Response
from .schema import (
    RegisterSchema, 
    VerifyOTPSchema, 
    ResendOPTSchema, 
    LoginSchema,
    ForgotPassSchema
)
from .service import (
    user_registration, 
    verify_otp, 
    resend_otp,
    user_login,
    user_logout,
    get_user_profile,
    user_password_forgot
)
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token import get_current_user, require_role
from app.utils.permissions import require_permission

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(req: RegisterSchema, db: Session = Depends(get_db)):
    return user_registration(req, db)


@router.post("/verify-otp")
async def verify_otp_route(req: VerifyOTPSchema, db: Session = Depends(get_db)):
    return verify_otp(req, db)


@router.post("/resend-otp")
async def resend_otp_route(req: ResendOPTSchema, db: Session = Depends(get_db)):
    return resend_otp(req, db)


@router.post('/login')
async def login_user(req: LoginSchema, res: Response, db: Session = Depends(get_db)):
    return user_login(req, res, db)


@router.post('/logout')
async def logout_user(res: Response, current_user: dict = Depends(get_current_user), ):
    return user_logout(res, current_user)


@router.post('/forgot-password')
async def forgot_password(req: ForgotPassSchema, db: Session = Depends(get_db)):
    return user_password_forgot(req, db)


@router.get('/me')
async def get_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_profile(current_user, db)


# @router.post('/foradimn')
# async def get_profile(current_user = Depends(require_role('customer'))):
#     return current_user
