from fastapi import status

from fastapi_localization.response import TranslateJsonResponse
from fastapi_localization.localization import lazy_gettext


async def http_exception_handler(request, exc):
    """
    Http exception handler with localization
    """
    status_code = exc.status_code if hasattr(exc, 'status_code') else status.HTTP_200_OK
    return TranslateJsonResponse({'detail': exc.detail, 'status_code': status_code})\
        .translate_content(request.state.gettext)


async def validation_exception_handler(request, exc):
    """
    Validation exception handler with localization
    """
    for error in exc.errors():
        error['msg'] = lazy_gettext(error['msg'])
    status_code = exc.status_code if hasattr(exc, 'status_code') else status.HTTP_200_OK
    return TranslateJsonResponse({"detail": exc.errors(), 'status_code': status_code}) \
        .translate_content(request.state.gettext)
