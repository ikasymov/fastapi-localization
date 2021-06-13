from typing import Callable

from fastapi import (
    Request,
    Response,
)
from fastapi.routing import APIRoute

from fastapi_localization.response import TranslateJsonResponse


class LocalizationRoute(APIRoute):
    """
    Route that localization response
    """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            if isinstance(response, TranslateJsonResponse):
                return response.translate_content(request.state.gettext)
            return response
        return custom_route_handler
