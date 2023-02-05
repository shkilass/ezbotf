"""
Defines almost all types for the framework work
"""

from .permissions import Permissions
from .context import Context

from typing import Any, Callable, Coroutine, Self
from telethon.events.raw import EventBuilder

__all__ = ['TOMLDict', 'PermissionsList', 'PermissionsDict', 'VersionSpecific', 'PLUGIN_REQUIREMENT_ONE_CHECK',
           'PLUGIN_REQUIREMENT_TWO_CHECKS', 'REQUIRED_PLUGINS_LIST', 'PluginEventFunction', 'PluginCommand']


TOMLDict = dict[str, Any]

PermissionsList  = list[str | Permissions]
PermissionsDict  = dict[str, PermissionsList]

VersionSpecific  = list[str, str, str]

PLUGIN_REQUIREMENT_ONE_CHECK   = list[str, list[str, str]]
PLUGIN_REQUIREMENT_TWO_CHECKS  = list[str, list[str, str], list[str, str]]
REQUIRED_PLUGINS_LIST          = list[PLUGIN_REQUIREMENT_ONE_CHECK | PLUGIN_REQUIREMENT_TWO_CHECKS]

PluginEventFunction = Callable[[Self], None]
PluginCommand       = Coroutine[EventBuilder, Context, None]
