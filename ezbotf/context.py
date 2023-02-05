"""
Defines :class:`Context` class that helps to store variables and transfer it between plugins,
and other framework elements.
"""

from . import reprutil
#from reprlib import recursive_repr

__all__ = ['Context']


class Context:
    """Class, that replaces dict with the sample namespace"""

    def __init__(self):
        pass

    def __str__(self):
        return self.__repr__()

    #@recursive_repr()
    def __repr__(self):
        return reprutil.get_repr(self)

    def has_value(self, value_name: str):
        """Checks, if value is have in this context

        :param value_name: String name of value to check

        :returns: True if value have in current context, otherwise False
        """

        return value_name in dir(self)
