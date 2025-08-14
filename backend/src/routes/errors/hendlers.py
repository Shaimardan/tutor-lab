from typing import Any

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from src.routes.errors.enum import EndpointErrorEnum


def serialize_error_details(exc_errors: Any) -> Any:
    if isinstance(exc_errors, list):
        return [serialize_error_details(err) for err in exc_errors]

    if isinstance(exc_errors, dict):
        new_dict = {}
        for k, v in exc_errors.items():
            if k == "ctx" and isinstance(v, dict):
                new_dict[k] = {
                    sub_k: str(sub_v) if isinstance(sub_v, Exception) else sub_v
                    for sub_k, sub_v in v.items()
                }
            else:
                new_dict[k] = serialize_error_details(v)
        return new_dict

    return exc_errors


async def http403_error_handler(
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        content={
            "error_code": EndpointErrorEnum.FORBIDDEN.name,
            "errors": EndpointErrorEnum.FORBIDDEN.value,
            "details": exc.detail,
        },
        status_code=HTTP_403_FORBIDDEN,
    )


async def http404_error_handler(
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        content={
            "error_code": EndpointErrorEnum.NOT_FOUND.name,
            "errors": EndpointErrorEnum.NOT_FOUND.value,
            "details": exc.detail,
        },
        status_code=HTTP_404_NOT_FOUND,
    )


async def http422_error_handler(
    exc: RequestValidationError | ValidationError,
) -> JSONResponse:
    errors = serialize_error_details(exc.errors())
    return JSONResponse(
        content={
            "error_code": EndpointErrorEnum.REQUEST_VALIDATION.name,
            "errors": EndpointErrorEnum.REQUEST_VALIDATION.value,
            "details": errors,
        },
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )
