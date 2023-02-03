"""
Defines type-hinted contexts
"""

import pathlib
import typing

from .context import Context

from telethon.types import User

if typing.TYPE_CHECKING:
    from .instance import BotInstance

__all__ = ['DirsContext', 'InstanceContext']


class DirsContext(Context):
    """Used for type-hint members of context

    :ivar plugins_dir: Directory with the plugins
    :ivar cache_dir: Directory with the cache
    :ivar logs_dir: Directory with the logs
    :ivar lang_dir: Directory with the translations
    :ivar permissions_dir: Directory with the permissions
    """

    plugins_dir: pathlib.Path | None      = None
    cache_dir: pathlib.Path | None        = None
    logs_dir: pathlib.Path | None         = None
    lang_dir: pathlib.Path | None         = None
    permissions_dir: pathlib.Path | None  = None


class InstanceContext(Context):
    """Used for type-hint members of context

    :ivar instance: Link to the current :class:`BotInstance`
    :ivar notifies: List with the notifies (`str`). It will send on any command from user and removed from list
    :ivar owner: User object (from the telethon, :class:`telethon.types.User`) of instance owner
    :ivar dirs: Context with all directories (:class:`DirsContext`)
    """

    instance: typing.Union['BotInstance', None]  = None
    notifies: list[str] | None                   = None
    owner: User | None                           = None
    dirs: DirsContext | None                     = None
