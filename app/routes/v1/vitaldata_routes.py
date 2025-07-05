from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix="/v1/vital",
    tags=["Vital"]
)

@router.websocket("/send")
async def get_data_to_store():
    # TODO: get data from Rafi & Pass to 
    pass