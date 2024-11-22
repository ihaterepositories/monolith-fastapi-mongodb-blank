from config import collection_name
from app.models.item import Item
from app.utils.serialization.item_serializer import serialize_individual, serialize_list
from app.utils.responses.response_creator import create_ok, create_error

from fastapi import APIRouter, Query, Body
from bson import ObjectId
from pymongo.errors import PyMongoError

item_router = APIRouter()

# GET all items
@item_router.get("/items")
async def get_items():

    try:
        items = serialize_list(collection_name.find())
        return create_ok("Items found", items)
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# GET a single item
@item_router.get("/item")
async def get_item(item_id: str = Query(None, description="Item ID to search")):

    if item_id is None:
        return create_error("Item ID is required", 400)
    
    try:
        item = serialize_individual(collection_name.find_one({"_id": ObjectId(item_id)}))
        return create_ok("Item found", item)
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# POST a new item
@item_router.post("/item")
async def post_item(item: Item = Body(..., description="Item to add")):

    if item is None:
        return create_error("Item is required", 400)
    
    try:
        collection_name.insert_one(item.model_dump())
        return create_ok("Item added successfully")
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# PUT an existing item
@item_router.put("/item")
async def put_item(
    item_id: str = Query(..., description="Item ID to update"), 
    updated_item: Item = Body(..., description="Updated item")
    ):

    if item_id is None:
        return create_error("Item ID is required", 400)
    
    if updated_item is None:
        return create_error("Updated item is required", 400)
    
    try:
        collection_name.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item.model_dump()})
        return create_ok("Item updated successfully")
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)

# DELETE an existing item
@item_router.delete("/item")
async def delete_item(item_id: str = Query(None, description="Item ID to delete")):

    if item_id is None:
        return create_error("Item ID is required", 400)
    
    try:
        collection_name.delete_one({"_id": ObjectId(item_id)})
        return create_ok("Item deleted successfully")
    except PyMongoError as e:
        return create_error(f"An error occurred: {e}", 500)
    except Exception as e:
        return create_error(f"An error occurred: {e}", 500)