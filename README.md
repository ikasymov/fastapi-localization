# fastapi_localization  [![Pytest Actions Status](https://github.com/ikasymov/fastapi-localization/workflows/pytest/badge.svg)](https://github.com/ikasymov/fastapi-localization/actions)

**fastapi_localization** - provides a simple language localization from Accept-Language header in your application.

Installation
```shell script
$ pip install fastapi-localization
```
Example with small fastapi application

```python
from typing import List

from pydantic import BaseModel
from fastapi_localization import TranslateJsonResponse
from fastapi_localization import TranslatableStringField

class LanguageTranslatableSchema(BaseModel):
    code: str
    title: TranslatableStringField


@app.get(
    '/language',
    response_class=TranslateJsonResponse,
    response_model=List[LanguageTranslatableSchema])
async def languages():
    return [{'code': 'ru', 'title': 'Russia'},
            {'code': 'en', 'title': 'English'}]
```
```shell script
# Russia
$ curl --location --request GET 'http://127.0.0.1:8000/language' \
--header 'Accept-Language: ru'

[{"code":"ru","title":"Русский"},{"code":"en","title":"Английский"}]


# English
$ curl --location --request GET 'http://127.0.0.1:8000/language' \
--header 'Accept-Language: en'

[{"code":"ru","title":"Russia"},{"code":"en","title":"English"}]
```

manual partial translation
```python
from fastapi_localization import TranslateJsonResponse
from fastapi_localization import lazy_gettext as _

@app.get(
    '/country',
    response_class=TranslateJsonResponse)
async def countries():
    return [{'code': 'ru', 'title': _('Russia')},
            {'code': 'us', 'title': 'USA'}]
```

```shell script
# Russian
$ curl --location --request GET 'http://127.0.0.1:8000/country' \
--header 'Accept-Language: ru'

[{"code":"ru","title":"Русский"},{"code":"us","title":"USA"}]


# English
$ curl --location --request GET 'http://127.0.0.1:8000/country' \
--header 'Accept-Language: en'

[{"code":"ru","title":"Russia"},{"code":"us","title":"USA"}]
```

error validation

```python
from pydantic import BaseModel, EmailStr
from fastapi_localization import TranslateJsonResponse

class InputSchema(BaseModel):
    email = EmailStr()


@app.post(
    '/input',
    response_class=TranslateJsonResponse)
async def countries(value: InputSchema):
    return value
```
```shell script
# Russia
$ curl --location --request POST 'http://127.0.0.1:8000/input' \
--header 'Accept-Language: ru' \
--header 'Content-Type: application/json' \
--data-raw '{"email": "invalid_email"}'

{
    "detail": [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "значение не является действительным адресом электронной почты",
            "type": "value_error.email"
        }
    ]
}


# English
$ curl --location --request POST 'http://127.0.0.1:8000/input' \
--header 'Accept-Language: en' \
--header 'Content-Type: application/json' \
--data-raw '{"email": "invalid_email"}'

{
    "detail": [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "value is not a valid email address",
            "type": "value_error.email"
        }
    ]
}
```

[Application](https://github.com/ikasymov/fastapi-localization-example) source code
