"""
Utility to get repr of any object
"""

from reprlib import recursive_repr

__all__ = ['get_repr']


@recursive_repr()
def get_repr(obj: object):
    """Get repr as Object(value1=..., value2=...) format

    :param obj: Object to repr

    :returns: String repr of the object
    """

    return f'{type(obj).__name__}({", ".join([f"{attr}={repr(getattr(obj, attr))}" for attr in dir(obj) if not attr.startswith("__")])})'
