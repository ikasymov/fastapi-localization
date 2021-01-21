import gettext
from typing import Callable
from unittest.mock import MagicMock

import pytest
from fastapi import Request


async def async_magic():
    pass


class AsyncMock(MagicMock):

    def __await__(self):
        return async_magic().__await__()


@pytest.fixture()
def mocked_request() -> Callable:

    def get_request(headers) -> Request:
        mocked = AsyncMock(spec=Request)
        mocked.headers = headers
        return mocked
    return get_request


@pytest.fixture()
def gettext_func():

    def get_gettext(language_code):
        gn = gettext.translation(
            'messages',
            localedir='tests/translations',
            languages=[language_code]
        )
        return gn.gettext
    return get_gettext
