"""
Defines base for type-casting. Use it module if you define custom argument type-caster
"""

from typing import Any

__all__ = ['ArgTypeCast', 'ListCast', 'DictCast', 'BoolCast']


class ArgTypeCast:
    """Base class to help with the type-casting

    :ivar type: Type to cast in
    """

    def __init__(self, type_: type):
        """
        :param type_: Type for the type-casting
        """
        self.type = type_

    def typecast(self, string: str) -> Any:
        """Type-cast string to the given type

        :param string: String to be type-casted

        :return: Type-casted object
        """

        return self.type(string)


class ListCast(ArgTypeCast):
    """Type-cast a string to the list

    :ivar splitter: Splitter to use
    :ivar values_type: Type to type-cast in values of list
    """

    def __init__(self, splitter: str = ', ', values_type: ArgTypeCast = ArgTypeCast(str)):
        """
        :param splitter: String splitter
        :param values_type: Type to cast the values of the list
        """
        super().__init__(list)

        self.splitter = splitter
        self.values_type = values_type

    def typecast(self, string: str) -> list[Any]:
        """Type-cast string to the list

        :param string: String to be type-casted

        :return: Type-casted list object
        """

        return [self.values_type.typecast(v) for v in string.split(self.splitter)]


class DictCast(ArgTypeCast):
    """Type-cast a string to the dict

    :ivar splitter: Splitter to split the (key=value) pairs
    :ivar kv_splitter: Splitter to split the key and value
    :ivar temp_char: Temp char to replace the '==' with it and back

    :ivar key_type: Type to type-cast the keys
    :ivar values_type: Type to type-cast the values
    """

    def __init__(self,
                 splitter: str = ', ',
                 kv_splitter: str = '=',
                 temp_char: str = '\uFFFF',
                 key_type: ArgTypeCast = ArgTypeCast(str),
                 values_type: ArgTypeCast = ArgTypeCast(str)):
        """
        :param splitter: Splitter to split the (key=value) pairs
        :param kv_splitter: Splitter to split the key and value
        :param temp_char: Temp char to replace the '==' with it and back

        :param key_type: Type to type-cast the keys
        :param values_type: Type to type-cast the values
        """
        super().__init__(dict)

        self.splitter = splitter
        self.kv_splitter = kv_splitter
        self.temp_char = temp_char

        self.key_type = key_type
        self.values_type = values_type

    def typecast(self, string: str) -> dict[Any, Any]:
        """Type-cast string to the dict

        :param string: String to be type-casted

        :return: Type-casted dict object
        """

        temp_cast = string.replace('==', self.temp_char)

        return {
            self.key_type.typecast((kvs := kv.split(self.kv_splitter))[0]):
                self.values_type.typecast(kvs[1].replace(self.temp_char, '=='))
            for kv in temp_cast.split(self.splitter)
        }


# define for the BoolCast
_true_list = ['yes', 'yea', '+', 'true']
_false_list = ['no', 'nop', '-', 'false']


class BoolCast(ArgTypeCast):
    """Type-cast a string to the bool

    :ivar true_list: List with the true string variants
    :ivar false_list: List with the false string variants
    :ivar match_case: Match case of the string
    """

    def __init__(self,
                 true_list: list[str] | None = None,
                 false_list: list[str] | None = None,
                 match_case: bool = False):
        """
        :param true_list: List with the true string variants
        :param false_list: List with the false string variants
        :param match_case: Match case of the string
        """
        super().__init__(dict)

        self.true_list = true_list if true_list is not None else _true_list
        self.false_list = false_list if false_list is not None else _false_list
        self.match_case = match_case

    def typecast(self, string: str) -> bool:
        """Type-cast string to the given type

        :param string: String to be type-casted

        :returns: Type-casted bool object

        :raises ArgumentTypeCastingError: When string isn't have in the true/false list
        """

        string_to_parse = string if self.match_case else string.lower()

        if string_to_parse in self.true_list:
            return True
        elif string_to_parse in self.false_list:
            return False
        else:
            raise ArgumentTypeCastingError(f'Can\'t type cast the string "{string}" to bool')
