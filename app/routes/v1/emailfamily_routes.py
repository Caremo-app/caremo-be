from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from ...util.jwt_generator import verify_token
from ...repositories.emailfamily_repositories import EmailFamilyRepository
from ...controllers.emailfamily_controllers import EmailFamilyController
from sqlalchemy.orm import Session

from ...util.use_db import get_db

router = APIRouter(
    prefix="/v1/family",
    tags=["Family"]
)

@router.get("/list")
async def get_family_personas(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    repo = EmailFamilyRepository(db)
    controller = EmailFamilyController(repo)
    return controller.get_family_personas(payload.sub)
    