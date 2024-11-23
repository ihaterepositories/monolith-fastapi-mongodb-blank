from config import items_collection
from app.models.item import Item
from app.utils.serialization.item_serializer import serialize_individual, serialize_list
from app.utils.responses.response_creator import create_ok, create_error

from fastapi import APIRouter, Query, Body
from bson import ObjectId
from pymongo.errors import PyMongoError
import redis.asyncio as redis
import json

item_router = APIRouter()
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# GET all items (sorting, limiting, skipping, caching)
@item_router.get("/items", summary="Get all items", description="Get all items from the database")
async def get_items(
    sort: str = Query(None, description="Sort items by field"),
    order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
    limit: int = Query(0, description="Limit the number of items to return"),
    skip: int = Query(0, description="Skip the first n items")
    ):

    cache_key = f"items:{sort}:{order}:{limit}:{skip}"
    cached_items = await redis_client.get(cache_key)
    if cached_items:
        return create_ok("Items found in cache", json.loads(cached_items))

    try:
        if sort is None:
            items = serialize_list(items_collection.find().limit(limit).skip(skip))
        else:
            items = serialize_list(items_collection.find().sort(sort, order).limit(limit).skip(skip))

        await redis_client.set(cache_key, json.dumps(items), ex=3600)
        return create_ok("Items found", items)
    
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# GET a single item (caching)
@item_router.get("/item", summary="Get a single item", description="Get a single item from the database")
async def get_item(item_id: str = Query(None, description="Item ID to search")):

    if item_id is None:
        return create_error("Item ID is required", 400)
    
    cache_key = f"item:{item_id}"
    cached_item = await redis_client.get(cache_key)
    if cached_item:
        return create_ok("Item found in cache", json.loads(cached_item))

    try:
        item = serialize_individual(items_collection.find_one({"_id": ObjectId(item_id)}))

        await redis_client.set(cache_key, json.dumps(item), ex=3600)
        return create_ok("Item found", item)
    
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# POST a new item
@item_router.post("/item", summary="Add a new item", description="Add a new item to the database")
async def post_item(item: Item = Body(..., description="Item to add")):

    if item is None:
        return create_error("Item is required", 400)
    
    try:
        items_collection.insert_one(item.model_dump())
        return create_ok("Item added successfully")
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# PUT an existing item
@item_router.put("/item", summary="Update an existing item", description="Update an existing item in the database")
async def put_item(
    item_id: str = Query(..., description="Item ID to update"), 
    updated_item: Item = Body(..., description="Updated item")
    ):

    if item_id is None:
        return create_error("Item ID is required", 400)
    
    if updated_item is None:
        return create_error("Updated item is required", 400)
    
    try:
        items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item.model_dump()})
        return create_ok("Item updated successfully")
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# DELETE an existing item
@item_router.delete("/item", summary="Delete an existing item", description="Delete an existing item from the database")
async def delete_item(item_id: str = Query(None, description="Item ID to delete")):

    if item_id is None:
        return create_error("Item ID is required", 400)
    
    try:
        items_collection.delete_one({"_id": ObjectId(item_id)})
        return create_ok("Item deleted successfully")
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)