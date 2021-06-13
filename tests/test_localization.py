from unittest.mock import MagicMock

from fastapi_localization.localization import (
    lazy_gettext,
    LazyString,
    prepare_content_to_translate,
    TranslatableStringField,
)


my_string = 'my message'
username = 'SomeUser'


def test_lazy_gettext():
    assert isinstance(lazy_gettext(my_string), LazyString)


def test_named_format_lazy_gettext():
    lazy = lazy_gettext(my_string, username=username)
    assert lazy.named_placeholders == {'username': username}
    assert isinstance(lazy, LazyString)


def test_translatable_string_field_validate():
    value = TranslatableStringField.validate(my_string)
    assert isinstance(value, TranslatableStringField)


def test_lazy_string():
    isinstance(LazyString(my_string), str)


def test_named_format_lasy_string():
    lazy_string = LazyString(my_string, name=username)
    assert lazy_string.named_placeholders == {'name': username}
    assert isinstance(lazy_string, str)


def test_prepare_content_translate(gettext_func):
    _ = gettext_func('ru')

    message = LazyString(my_string)
    content = [dict(message=message), dict(message=message)]

    expected_result = [{'message': 'Мое сообщение'}, {'message': 'Мое сообщение'}]
    result = prepare_content_to_translate(content, _)
    assert result == expected_result


def test_prepare_content_translate_named_format(gettext_func):
    _ = gettext_func('ru')
    message = LazyString('This message for {name}', name=username)
    content = [dict(message=message), dict(message=message)]

    expected_result = [
        {'message': f'Это сообщение для {username}'},
        {'message': f'Это сообщение для {username}'},
    ]
    result = prepare_content_to_translate(content, _)
    assert result == expected_result


def test_prepare_content_called_gettext():
    message = LazyString(my_string)
    content = [dict(message=message), dict(message=message)]

    mock = MagicMock()
    prepare_content_to_translate(content, mock)
    assert mock.call_count == 2
