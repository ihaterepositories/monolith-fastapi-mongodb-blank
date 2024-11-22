from fastapi import FastAPI
from app.routes.item_route import item_router

app = FastAPI()

app.include_router(item_router)
