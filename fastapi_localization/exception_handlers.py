from fastapi import (
    HTTPException,
    status,
)
from fastapi.exceptions import RequestValidationError

from fastapi_localization.localization import lazy_gettext
from fastapi_localization.response import TranslateJsonResponse


async def http_exception_handler(request, exc: HTTPException):
    """
    Http exception handler with localization
    """
    response = TranslateJsonResponse(
        {'detail': exc.detail},
        status_code=exc.status_code
    )
    return response.translate_content(request.state.gettext)


async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Validation exception handler with localization
    """
    for error in exc.errors():
        error['msg'] = lazy_gettext(error['msg'])
    response = TranslateJsonResponse(
        {"detail": exc.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    return response.translate_content(request.state.gettext)
