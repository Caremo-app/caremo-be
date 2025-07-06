from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from .routes.main_routes import router
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from .routes.v1.vitaldata_routes import manager

from .db.database import Base, engine, SessionLocal

# Initiate App
app = FastAPI()

# Initialize DBs
Base.metadata.create_all(bind=engine)

# middlewares
app.add_middleware(SessionMiddleware, secret_key="edbert1234")

# HealthCheck
@app.get("/")
async def root():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.websocket("/ws/send/{client_id}")
async def get_data_to_store(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
        
# ALL ROUTES 
app.include_router(router, prefix="/api")