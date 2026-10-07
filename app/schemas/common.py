from __future__ import annotations

from typing import Any, Optional
from pydantic import Field
from sqlmodel import SQLModel


class BaseResponse(SQLModel):
    code: int = Field(default=200, description="HTTP status code")
    message: str = Field(..., description="Human-readable response message")
    data: Optional[Any] = Field(default=None, description="Response payload data")

    model_config = {
        "json_schema_extra": {
            "example": {
                "code": 200,
                "message": "Operation completed successfully",
                "data": {"id": 1, "status": "active"}
            }
        }
    }
