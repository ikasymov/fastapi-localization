from fastapi_localization import TranslateJsonResponse
from fastapi_localization.localization import lazy_gettext as _


def test_translate_response_content(gettext_func):
    gettext = gettext_func('ru')

    content = {
        'message': _('my message'),
    }
    translated_content = (
        TranslateJsonResponse(content)
        .translate_content(gettext)
        .original_content
    )
    expected_content = {'message': 'Мое сообщение'}
    assert translated_content == expected_content
