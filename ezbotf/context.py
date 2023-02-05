"""
Defines :class:`Context` class that helps to store variables and transfer it between plugins,
and other framework elements.
"""

__all__ = ['Context']


class Context:
    """Class, that replaces dict with the sample namespace"""

    def __init__(self):
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Context({" ".join([f"{attr}={repr(getattr(self, attr))}" for attr in dir(self) if not attr.startswith("__")])})'

    def has_value(self, value_name: str):
        """Checks, if value is have in this context

        :param value_name: String name of value to check

        :returns: True if value have in current context, otherwise False
        """

        return value_name in dir(self)
