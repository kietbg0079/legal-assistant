from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from .v1 import v1_router

versions = {
    "v1": v1_router
}


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(versions["v1"])
