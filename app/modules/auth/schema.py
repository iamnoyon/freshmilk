import re

from pydantic import BaseModel, Field, field_validator
from enum import Enum


class AreaEnum(str, Enum):
    MIRPURDOSH = "mirpurdosh"


class RegisterSchema(BaseModel):
    name: str = Field(default="Mr. John", min_length=2, max_length=100)
    nid: str = Field(default="12324353432", min_length=10, max_length=20)
    phone: str = Field(default="01889010235", min_length=11, max_length=15)
    password: str = Field(default="1234", min_length=4, max_length=4)
    area: AreaEnum = AreaEnum.MIRPURDOSH
    road: str = Field(default="10", min_length=1, max_length=20)
    house: str = Field(default="1234", min_length=1, max_length=20)
    flat: str = Field(default="A5", min_length=1, max_length=20)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?\d+$", v):
            raise ValueError("Phone must contain only digits, optionally starting with +")
        return v


class VerifyOTPSchema(BaseModel):
    phone: str = Field(..., min_length=11, max_length=15)
    otp: str = Field(..., min_length=5, max_length=5)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?\d+$", v):
            raise ValueError("Phone must contain only digits, optionally starting with +")
        return v

    @field_validator("otp")
    @classmethod
    def validate_otp(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("OTP must contain only digits")
        return v



class ResendOPTSchema(BaseModel):
    phone: str = Field(..., min_length=11, max_length=15)



class LoginSchema(BaseModel):
    phone: str = Field(default="01889010235", min_length=11, max_length=15)
    password: str = Field(default="1234", min_length=4, max_length=4)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?\d+$", v):
            raise ValueError("Phone must contain only digits, optionally starting with +")
        return v


class ForgotPassSchema(BaseModel):
    phone: str = Field(default="01889010235", min_length=11, max_length=15)
