import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_localization import SystemLocalizationMiddleware
from fastapi_localization.route import LocalizationRoute
from fastapi_localization.response import TranslateJsonResponse
from fastapi_localization.localization import lazy_gettext as _

app = FastAPI()
client = TestClient(app)
app.router.route_class = LocalizationRoute
localization_middleware = SystemLocalizationMiddleware(
        domain='messages',
        translation_dir='tests/translations',
)
app.add_middleware(BaseHTTPMiddleware, dispatch=localization_middleware)


@app.get('/', response_class=TranslateJsonResponse)
async def index():
    return {
        'message': _('My page')
    }


def test_route_call_json_response():
    response = client.get('/', headers={'accept-language': 'ru'})
    expected_content = {'message': 'Моя страница'}
    assert json.loads(response.content) == expected_content
