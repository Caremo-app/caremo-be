from fastapi import APIRouter
from .v1.user_routes import router as user_router
from .v1.auth_routes import router as auth_router
from .v1.emailfamily_routes import router as emailfamily_router
from .v1.ai_routes import router as ai_router

router = APIRouter()

# for v1 user router
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(emailfamily_router)
router.include_router(ai_router)