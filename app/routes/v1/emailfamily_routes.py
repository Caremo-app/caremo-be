from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from ...util.jwt_generator import verify_token
from ...repositories.emailfamily_repositories import EmailFamilyRepository
from ...controllers.emailfamily_controllers import EmailFamilyController
from ...repositories.persona_repositories import PersonaRepository
from ...controllers.persona_controllers import PersonaController
from ...schemas.persona_schema import PersonaCreateSchema
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
    return controller.get_family_personas(payload['sub'])

@router.post("/personas")
async def add_family_personas(persona_data: PersonaCreateSchema, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    controller = PersonaController(db)
    return controller.create_persona(persona_data)
    