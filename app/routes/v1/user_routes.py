from fastapi import APIRouter
from ...controllers.user_controllers import get_users_controller

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)

@router.get("/user")
async def get_users():
    return await get_users_controller()