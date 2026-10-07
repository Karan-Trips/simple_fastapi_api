from __future__ import annotations

import logging
from typing import Any, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_response(code: int, message: str, data: Optional[Any] = None) -> JSONResponse:
    response_content = {
        "code": code,
        "message": message,
        "data": jsonable_encoder(data) if data is not None else {},
    }
    logger.debug(f"API Response [{code}]: {message}")
    return JSONResponse(status_code=code, content=response_content)


def create_success_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=200, message=message, data=data)


def create_created_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=201, message=message, data=data)


def create_no_content_response() -> JSONResponse:
    return JSONResponse(status_code=204, content=None)


def create_error_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=400, message=message, data=data)


def create_bad_request_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=400, message=message, data=data)


def create_unauthorized_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=401, message=message, data=data)


def create_forbidden_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=403, message=message, data=data)


def create_not_found_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=404, message=message, data=data)


def create_conflict_response(message: str = "Conflict occurred", data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=409, message=message, data=data)


def create_unprocessable_entity_response(message: str = "Unprocessable entity", data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=422, message=message, data=data)


def create_too_many_requests_response(message: str = "Too many requests", data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=429, message=message, data=data)


def create_server_error_response(message: str, data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=500, message=message, data=data)


def create_not_implemented_response(message: str = "Not implemented", data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=501, message=message, data=data)


def create_service_unavailable_response(message: str = "Service unavailable", data: Optional[Any] = None) -> JSONResponse:
    return create_response(code=503, message=message, data=data)
