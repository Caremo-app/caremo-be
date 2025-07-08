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

# ALL ROUTES 
app.include_router(router, prefix="/api")