from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

# from  import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.VERSION,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"msg": "hello world"}


@app.get("/info")
async def get_info():
    return {
        "app_name": settings.app_name,
        "version": settings.VERSION,
        "api_version": settings.API_V,
        "database_url": settings.DATABASE_URL,
    }
