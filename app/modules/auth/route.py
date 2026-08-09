from fastapi import APIRouter, Depends
from .schema import RegisterSchema, VerifyOTPSchema, ResendOPTSchema
from .service import user_registration, verify_otp
from app.core.db import get_db
from sqlalchemy.orm import Session

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
