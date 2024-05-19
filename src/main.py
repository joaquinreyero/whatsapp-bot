from fastapi import FastAPI

from src.api import webhook

app = FastAPI()

app.include_router(webhook.router)
