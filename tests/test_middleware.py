import gettext

import pytest
from fastapi import Request

from fastapi_localization.middleware import SystemLocalizationMiddleware


@pytest.mark.asyncio
async def test_set_gettext_to_request_state(mocked_request):
    request: Request = mocked_request({'accept-language': 'ru'})
    middleware = SystemLocalizationMiddleware('base', 'locales')
    await middleware(request, lambda x: x)

    assert callable(request.state.gettext)
    assert request.state.gettext == gettext.gettext
