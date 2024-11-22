from app.utils.responses.models.base_response import BaseResponse

from fastapi import HTTPException
from typing import Any

def create_ok(message: str, data: Any = None) -> BaseResponse:
    return BaseResponse(
        status_code=200,
        message=message,
        data=data
    )

def create_error(message: str, status_code: int = 400) -> BaseResponse:
    raise HTTPException(
        status_code=status_code,
        detail=BaseResponse(status_code=status_code, message=message).model_dump()
    )