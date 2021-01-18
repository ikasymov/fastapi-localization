import gettext
import typing


class LazyString(str):
    """
    LazyString object to localization
    """
    pass


class TranslatableStringField(LazyString):
    """
    Object for register localization
    Use like pydantic type.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return cls(v)


def lazy_gettext(string: str):
    """
    lazy gettext wrapper.
    """
    return LazyString(string)


def prepare_content_to_translate(value: typing.Any, _: gettext.gettext):
    """
    Prepare data structure to localization
    """
    if isinstance(value, LazyString):
        return str(_(value))
    elif isinstance(value, dict):
        return {
            k: prepare_content_to_translate(
                v,
                _
            )
            for k, v in value.items()
        }
    elif isinstance(value, list):
        return [
            prepare_content_to_translate(
                item,
                _
            )
            for item in value
        ]
    return value


def get_gettext(
        domain: str, localedir: str, language_code: str = None
):
    """
    Get gettext func by locale or default gettext
    """
    try:
        gnu = gettext.translation(
            domain,
            localedir=localedir,
            languages=[language_code]
        )
        return gnu.gettext
    except (FileNotFoundError, AttributeError):
        return gettext.gettext
