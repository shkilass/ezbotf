.. _pluginloader:

.. currentmodule:: ezbotf

===================
pluginloader module
===================

.. note:: This module is imports as ``from .. import *``. This means that there
    is no need to import it separately or use ``ezbotf.pluginloader.PluginManageFunction``.
    You can simply use ``ezbotf.PluginLoader`` as example.

.. automodule:: ezbotf.pluginloader

PluginManageFunction
====================

A type-hint for the functions, that required for :func:`PluginLoader.apply_on_plugins()`

PluginLoader
============

:class:`PluginLoader` is used for manage plugins and load it (as can guess from it name).
You mustn't to manually use it, use :class:`BotInstance`.

.. autoclass:: PluginLoader

    .. automethod:: __init__

    .. automethod:: initialize

    .. automethod:: import_plugin

    .. automethod:: initialize_plugins

    .. automethod:: load_plugin

    .. automethod:: unload_plugin

    .. automethod:: start_plugin

    .. automethod:: reload_plugin

    .. automethod:: apply_on_plugins

    .. automethod:: load_plugins

    .. automethod:: unload_plugins

    .. automethod:: start_plugins

    .. automethod:: get_command
