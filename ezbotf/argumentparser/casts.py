"""
Defines initialized type-casts objects. Use it in Argument type definition
"""

from . import _casts

__all__ = ['Cast', 'ListCast', 'DictCast']


class Cast:
    """Initialized ArgTypeCast casts

    :ivar StrCast: Cast to the ``str`` type
    :ivar StrCast: Cast to the ``int`` type
    :ivar StrCast: Cast to the ``float`` type
    :ivar StrCast: Cast to the ``bool`` type (have type of :class:`_casts.BoolCast`)
    """

    StrCast = _casts.ArgTypeCast(str)
    IntCast = _casts.ArgTypeCast(int)
    FloatCast = _casts.ArgTypeCast(float)
    BoolCast = _casts.BoolCast()

    @staticmethod
    def setup_bool_cast_translations(true_list: list[str], false_list: list[str]):
        """Set up the BoolCast type-cast translations

        :param true_list: List with the true string variants
        :param false_list: List with the false string variants
        """

        Cast.BoolCast = _casts.BoolCast(true_list, false_list)


class ListCast:
    """Initialized ListCast casts.
    Usage example: ez example value1, value2, value3, ...

    :ivar ListStrCast: Cast to the ``list[str]`` type
    :ivar ListIntCast: Cast to the ``list[int]`` type
    :ivar ListFloatCast: Cast to the ``list[float]`` type
    :ivar ListBoolCast: Cast to the ``list[bool]`` type
    """

    ListStrCast = _casts.ListCast()
    ListIntCast = _casts.ListCast(values_type=Cast.IntCast)
    ListFloatCast = _casts.ListCast(values_type=Cast.FloatCast)
    ListBoolCast = _casts.ListCast(values_type=Cast.BoolCast)


class DictCast:
    """Initialized DictCast casts.
    Usage example: ez example key1=value2, key2=value2, ...

    :ivar DictStrStrCast: Cast to the ``dict[str, str]`` type
    :ivar DictStrIntCast: Cast to the ``dict[str, int]`` type
    :ivar DictStrFloatCast: Cast to the ``dict[str, float]`` type
    :ivar DictStrBoolCast: Cast to the ``dict[str, bool]`` type

    :ivar DictIntStrCast: Cast to the ``dict[int, str]`` type
    :ivar DictIntIntCast: Cast to the ``dict[int, int]`` type
    :ivar DictIntFloatCast: Cast to the ``dict[int, float]`` type
    :ivar DictIntBoolCast: Cast to the ``dict[int, bool]`` type
    """

    DictStrStrCast = _casts.DictCast()
    DictStrIntCast = _casts.DictCast(values_type=Cast.IntCast)
    DictStrFloatCast = _casts.DictCast(values_type=Cast.FloatCast)
    DictStrBoolCast = _casts.DictCast(values_type=Cast.BoolCast)

    DictIntStrCast = _casts.DictCast(key_type=Cast.IntCast)
    DictIntIntCast = _casts.DictCast(key_type=Cast.IntCast, values_type=Cast.IntCast)
    DictIntFloatCast = _casts.DictCast(key_type=Cast.IntCast, values_type=Cast.FloatCast)
    DictIntBoolCast = _casts.DictCast(key_type=Cast.IntCast, values_type=Cast.BoolCast)
