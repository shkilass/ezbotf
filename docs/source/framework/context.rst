.. _context:

.. currentmodule:: ezbotf

==============
context module
==============

.. note:: This module is imports as ``from .. import *``. This means that there
    is no need to import it separately or use ``ezbotf.context.Context``.
    You can simply use ``ezbotf.Context`` as example.

.. automodule:: ezbotf.context

Context
=======

.. autoclass:: Context

    .. automethod:: has_value

Other methods, such as `__init__()`, `__repr()__` isn't interested and not documented.
But, in the :class:`Context` have one feature. When you print it, it prints out all it
members by usage a :func:`repr()` function. Example is bottom.

.. code-block:: python

    ...
    plugin.logger.debug(repr(plugin.context))  # or: plugin.logger.debug(plugin.context)
    ...

It will print something that:

.. code-block:: python

    Context(cache_dir=WindowsPath('cache') dirs=Context(cache_dir=WindowsPath('cache') lang_dir=WindowsPath('lang') logs_dir=WindowsPath('logs') permissions_dir=WindowsPath('permissions') plugins_dir=WindowsPath('plugins')) instance=<ezbotf.instance.BotInstance object at 0x000001AD635DA990> notifies=['⚠️ Version **1.0.0b3 [unstable]** of `EzBot Framework` is unstable. This may cause problems!'] owner=None)
