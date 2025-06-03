from typing import Union
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from loguru import logger  # Add this import


def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    log_kwargs = {}
    if exc.status_code >= 500:
        log_kwargs["exc_info"] = True  # Include stack trace for server errors
        logger.error(
            f"HTTPException: Status: {exc.status_code}, Detail: {exc.detail}", **log_kwargs
        )
    else:
        # For client errors (4xx), stack trace is usually not needed
        logger.warning(f"HTTPException: Status: {exc.status_code}, Detail: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail if exc.detail else "HTTP error"},
    )


def http422_error_handler(
    _: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    errors = []
    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
    elif isinstance(exc, ValidationError):
        errors = exc.errors()

    logger.warning(f"RequestValidationError (422): Details: {errors}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


# Modify the default validation error response structure in OpenAPI docs
validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}
