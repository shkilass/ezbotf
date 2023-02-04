.. _exceptions:

.. currentmodule:: ezbotf.exceptions

=================
exceptions module
=================

.. note:: This module is imports as ``from .. import exceptions``. This means that you
     must use ``ezbotf.exceptions.PluginError`` as example.

.. automodule:: ezbotf.exceptions

PluginError
===========

.. autoclass:: PluginError

    .. automethod:: __init__

    Example for plugin:

    .. code-block:: python

        import ezbotf

        plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)


        class SpecialFailError(ezbotf.exceptions.PluginError):

            def __init__(self):
                super().__init__('specially failed for the example')
                # NOTE: This will be interpreted as:
                # >>> MyPlugin.SpecialFailError: Plugin "FailPlugin" specially failed for the example

        @plugin.on_load
        def on_load():

            @plugin.command('forcefail')
            async def forcefail(event, args):
                raise SpecialFailError()  # Raise our error

                # You can also use:
                # raise ezbotf.exceptions.PluginError('specially failed for the example')

IncorrectInstanceConfigError
============================

.. autoclass:: IncorrectInstanceConfigError

    .. automethod:: __init__

    .. note:: This exception is only used if config given to instance is incorrect
