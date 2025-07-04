from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .routes.main_routes import router
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

# Initiate App
app = FastAPI()

# middlewares
app.add_middleware(SessionMiddleware, secret_key="edbert1234")

# HealthCheck
@app.get("/")
async def root():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# ALL ROUTES 
app.include_router(router, prefix="/api")