from fastapi import APIRouter

from app.modules.auth.route import router as auth_routes
from app.modules.user.route import router as user_routes 

router = APIRouter()

router.include_router(auth_routes)
router.include_router(user_routes)