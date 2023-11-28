from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth import router as auth_router
from src.config import ALLOWED_ORIGINS
from src.search.views import router as search_router

app = FastAPI(title="ZRECENZOWANE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_router)
app.include_router(router=search_router)
