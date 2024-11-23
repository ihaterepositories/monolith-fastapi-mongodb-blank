from app.utils.responses.models.base_response import BaseResponse
from app.utils.logging.logger_creator import setup_logger

from fastapi import HTTPException
from typing import Any

logger = setup_logger("response_logger", "logs/response_logs.log")

def create_ok(message: str, data: Any = None) -> BaseResponse:
    logger.info(f"{message}")
    return BaseResponse(
        status_code=200,
        message=message,
        data_count=len(data) if data is not None else 0,
        data=data
    )

def create_error(message: str, status_code: int = 400) -> BaseResponse:
    logger.error(f"{message}")
    raise HTTPException(
        status_code=status_code,
        detail=BaseResponse(status_code=status_code, message=message).model_dump()
    )