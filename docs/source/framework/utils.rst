.. _utils:

.. currentmodule:: ezbotf.utils

============
utils module
============

.. note:: This module is imports as ``from .. import utils``. This means that you
     must use ``ezbotf.utils.check_config`` as example.

System functions
================

These utility functions is created for framework base.

.. autofunction:: check_config

.. autofunction:: check_config_by_path

.. autofunction:: get_translator_for_plugin

.. autofunction:: load_runtime_config

Requirement management functions
================================

This usable for the plugins ``on_install`` event. These functions that implements functiona of
of installing requirements and checking required plugins.

.. seealso:: :func:`ezbotf.Plugin.on_install()` - Example with utilities usage

.. autofunction:: install_requirements_by_path

.. autofunction:: install_requirements

.. autofunction:: check_required_plugins_by_list

.. autofunction:: check_required_plugins

Permission management functions
===============================

There is functions to load\save permissions and check permissions for some user.

.. autofunction:: load_permissions

.. autofunction:: save_permissions

.. autofunction:: have_permissions

Other
=====

.. autofunction:: run_coroutine_without_await

.. autofunction:: compare_versions

.. autofunction:: mask_phone_number

.. autofunction:: sort_by_priority
