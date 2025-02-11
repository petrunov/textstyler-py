# main.py
from fastapi import FastAPI

from app.routes.text_improvement import router as text_router

app = FastAPI()

app.include_router(text_router)
