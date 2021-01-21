from unittest.mock import MagicMock

from fastapi_localization.localization import (
    LazyString,
    TranslatableStringField,
    prepare_content_to_translate,
    lazy_gettext
)

my_string = 'my message'


def test_lazy_gettext():
    assert isinstance(lazy_gettext(my_string), LazyString)


def test_translatable_string_field_validate():
    value = TranslatableStringField.validate(my_string)
    assert isinstance(value, TranslatableStringField)


def test_lazy_string():
    isinstance(LazyString(my_string), str)


def test_prepare_content_translate(gettext_func):
    _ = gettext_func('ru')

    message = LazyString(my_string)
    content = [dict(message=message), dict(message=message)]

    expected_result = [{'message': 'Мое сообщение'}, {'message': 'Мое сообщение'}]
    result = prepare_content_to_translate(content, _)
    assert result == expected_result


def test_prepare_content_called_gettext():
    message = LazyString(my_string)
    content = [dict(message=message), dict(message=message)]

    mock = MagicMock()
    prepare_content_to_translate(content, mock)
    assert mock.call_count == 2



