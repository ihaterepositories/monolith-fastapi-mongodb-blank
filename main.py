from app.routes.item_route import item_router
from config import REDIS_URI

from fastapi import FastAPI
import redis.asyncio as redis

app = FastAPI()

app.include_router(item_router)

redis_client = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    print("Connected to Redis")

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
