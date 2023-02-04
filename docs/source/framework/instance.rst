.. _instance:

.. currentmodule:: ezbotf

===============
instance module
===============

.. note:: This module is imports as ``from .. import *``. This means that there
    is no need to import it separately or use ``ezbotf.instance.BotInstance``.
    You can simply use ``ezbotf.BotInstance`` as example.

.. automodule:: ezbotf.instance

BotInstance
===========

The :class:`BotInstance` is main class of all. Instance of it class
manages all required things, as: PluginManager, Context, etc. Also, handles
a messages from the Telegram (method: :func:`BotInstance.handle_message()`)

**Quick usage of this class:**

.. code-block:: python

    import ezbotf
    from pathlib import Path

    instance = ezbotf.BotInstance()
    instance.import_config(Path('<PATH TO THE CONFIG OF INSTANCE>'))  # Set ups config
    instance.quick_run()  # Calls all required methods to start an instance

.. note:: You must create a file with the configuration of instance. See
    :ref:`Instance Configuration <instance-configuration>` about this.

.. autoclass:: BotInstance

    .. automethod:: __init__

    .. automethod:: import_config

    .. automethod:: setup_context

    .. automethod:: initialize

    .. automethod:: load

    .. automethod:: run

    .. automethod:: quick_run

    .. automethod:: handle_message
