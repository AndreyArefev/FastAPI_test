from fastapi import APIRouter

from app.api import (
    auth,
    admin,
    user,
)

router = APIRouter()
router.include_router(auth.router)
router.include_router(admin.router)
router.include_router(user.router)