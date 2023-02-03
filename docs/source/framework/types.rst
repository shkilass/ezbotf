.. _types:

.. currentmodule:: ezbotf.types

============
types module
============

.. automodule:: ezbotf.types

    ``TOMLDict = dict[str, Any]``

        Alias to ``dict[str, Any]``

    ``PermissionsList = list[str | ezbotf.Permissions]``

        Alias to ``list[str | ezbotf.Permissions]``

    ``PermissionsDict = dict[int, PermissionsList]``

        Alias to ``dict[int, PermissionsList]`` or ``dict[int, list[str | ezbotf.Permissions]]``

    ``VersionSpecific = dict[str, Any]``

        Alias to ``dict[str, Any]``

    ``PLUGIN_REQUIREMENT_ONE_CHECK = list[str, list[str, str]]``

        Alias to ``list[str, list[str, str]]``

    ``PLUGIN_REQUIREMENT_TWO_CHECKS = list[str, list[str, str], list[str, str]]``

        Alias to ``list[str, list[str, str], list[str, str]]``

    ``REQUIRED_PLUGINS_LIST = list[PLUGIN_REQUIREMENT_ONE_CHECK | PLUGIN_REQUIREMENT_TWO_CHECKS]```

        Alias to ``list[PLUGIN_REQUIREMENT_ONE_CHECK | PLUGIN_REQUIREMENT_TWO_CHECKS]`` or
        ``list[list[str, list[str, str]] | list[str, list[str, str], list[str, str]]]``

        .. note:: This is scary

    ``PluginEventFunction = Callable[[Self], None]``

        Alias to ``Callable[[Self], None]``

    ``PluginCommand = Coroutine[EventBuilder, Context, None]``

        Alias to ``Coroutine[EventBuilder, Context, None]``
