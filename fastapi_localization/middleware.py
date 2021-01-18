from fastapi import Request

from fastapi_localization.localization import get_gettext


class SystemLocalizationMiddleware:
    """
    Middleware that creates gettext.GNUTranslations.gettext by Accept-Language
    and save to request.state.
    """
    def __init__(
            self,
            domain: str,
            translation_dir: str
    ):
        self.translation_dir = translation_dir
        self.domain = domain

    async def __call__(self, request: Request, call_next):
        language_code = request.headers.get('accept-language')

        if language_code:
            language_code = language_code.split(',')[0]
        request.state.gettext = get_gettext(
            self.domain,
            self.translation_dir,
            language_code
        )

        response = await call_next(request)
        return response


