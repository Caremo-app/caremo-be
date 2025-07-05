from fastapi import APIRouter

router = APIRouter(
    prefix='/v1/ai',
    tags=['AI']
)

@router.post("/infer")
async def get_infer_ai():
    #TODO : Konek Dengan AKMAL
    pass