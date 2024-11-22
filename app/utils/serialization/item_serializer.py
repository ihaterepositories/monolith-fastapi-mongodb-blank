def serialize_individual(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item["description"]
    }

def serialize_list(items) -> list:
    return [serialize_individual(item) for item in items]