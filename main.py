from app.routes.item_route import item_router
from config import REDIS_HOST, REDIS_PORT

from fastapi import FastAPI
import redis.asyncio as redis

app = FastAPI()

app.include_router(item_router)

redis_client = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print("INFO:     Connected to Redis successfully")

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
