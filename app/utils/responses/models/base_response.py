from pydantic import BaseModel
from typing import Any, List, Optional

class BaseResponse(BaseModel):
    status_code: Optional[int]
    message: str
    data: Optional[Any] = None

    
    
