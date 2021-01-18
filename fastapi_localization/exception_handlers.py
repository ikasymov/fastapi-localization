from fastapi_localization.response import TranslateJsonResponse
from fastapi_localization.localization import lazy_gettext


async def http_exception_handler(request, exc):
    """
    Http exception handler with localization
    """
    return TranslateJsonResponse({'detail': exc.detail})\
        .translate_content(request.state.gettext)


async def validation_exception_handler(request, exc):
    """
    Validation exception handler with localization
    """
    for error in exc.errors():
        error['msg'] = lazy_gettext(error['msg'])
    return TranslateJsonResponse({"detail": exc.errors()}) \
        .translate_content(request.state.gettext)
