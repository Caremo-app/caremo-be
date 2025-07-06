from fastapi import APIRouter
from .v1.vitaldata_routes import router as vitaldata_router

router = APIRouter()
