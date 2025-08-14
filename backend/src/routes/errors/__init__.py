from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from src.routes.errors.hendlers import (
    http403_error_handler,
    http404_error_handler,
    http422_error_handler,
)


async def base_http_exception_handler(
    _: Request,
    exc: HTTPException | Exception | RequestValidationError | ValidationError,
) -> JSONResponse:
    if isinstance(exc, (RequestValidationError, ValidationError)):
        return await http422_error_handler(exc)
    elif isinstance(exc, HTTPException):
        http_status = exc.status_code
        match http_status:
            case 403:
                return await http403_error_handler(exc)
            case 404:
                return await http404_error_handler(exc)
            case _:
                return JSONResponse(
                    content={
                        "error_code": exc.status_code,
                        "errors": exc.status_code,
                        "details": exc.detail,
                    },
                    status_code=exc.status_code,
                )

    return JSONResponse(status_code=500, content=exc)
