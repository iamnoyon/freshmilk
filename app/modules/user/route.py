from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile")
async def get_user_profile():
    return {"message": "User profile information"}