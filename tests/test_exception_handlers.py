import json

import pytest
from fastapi import (
    Request,
    status,
)
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from fastapi_localization.exception_handlers import (
    http_exception_handler,
    validation_exception_handler
)
from fastapi_localization.localization import lazy_gettext


@pytest.mark.asyncio
async def test_http_exception_handler(mocked_request, gettext_func):
    _ = gettext_func('ru')
    request: Request = mocked_request(dict())
    request.state.gettext = _
    exc = HTTPException(detail=lazy_gettext('my error'), status_code=status.HTTP_400_BAD_REQUEST)

    response = await http_exception_handler(request, exc)
    expected_data = {'detail': 'моя ошибка'}
    assert json.loads(response.body) == expected_data
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_validation_exception_handler(mocked_request, gettext_func):
    _ = gettext_func('ru')
    request: Request = mocked_request(dict())
    request.state.gettext = _

    class Model(BaseModel):
        a: int

    with pytest.raises(ValidationError) as exc:
        Model(a='snap')

    response = await validation_exception_handler(request, exc.value)
    expected_data = {'detail': [
        {'loc': ('a',),
         'msg': 'значение не является числом',
         'type': 'type_error.integer'}
    ]}
    assert response.original_content == expected_data
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
