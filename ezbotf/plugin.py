"""
Defines the :class:`PluginType`, :class:`Plugin` classes that helps to create plugins on the EzBot Framework.
"""

import pathlib

from . import ezlog
from .context import Context
from .translator import Translator
from .argumentparser import ArgumentParser, Argument
from .permissions import Permissions
from .instancecontext import InstanceContext

from .types import TOMLDict, PluginEventFunction, PluginCommand
from enum import Enum, auto
from typing import Self, Any, Coroutine, Callable

__all__ = ['PluginType', 'Plugin']


class PluginType(Enum):
    """Enum of the plugin types

    :ivar CoreLibrary: Marks plugin as Core Library
    :ivar Core: Marks plugin as Core
    :ivar Library: Marks plugin as Library
    :ivar Standalone: Marks plugin as Standalone
    """

    CoreLibrary  = auto()
    Core         = auto()
    Library      = auto()
    Standalone   = auto()


class Plugin:
    """Class of the plugins

    :ivar type: Type of the plugin
    :ivar logger: Logger of the plugin
    :ivar context: Link to the working context (:class:`InstanceContext`)
    :ivar translator: :class:`Translator` instance
    :ivar dir: Path to the plugin directory
    :ivar runtime_config: TOML dictionary with the runtime config
    :ivar loaded: Plugin is loaded? When plugin is not loaded, almost all variables is None
    :ivar enabled: Plugin is enabled? When plugin is disabled, all commands and other will not work
    :ivar failed: Plugin is failed? When plugin is failed, it works as disabled. Failing is going on exceptions
    :ivar commands: Dictionary with the commands of the plugin
    :ivar mod: Module of this plugin
    :ivar on_install_funcs: List with the binders to on_install event
    :ivar on_setup_funcs: List with the binders to on_setup event
    :ivar on_load_funcs: List with the binders to on_load event
    :ivar on_unload_funcs: List with the binders to on_unload event
    :ivar on_start_funcs: List with the binders to on_start event
    """

    def __init__(self, type_: PluginType = PluginType.Standalone):
        """
        :param type_: Type of the plugin
        """

        self.type = type_

        self.logger: ezlog.Logger | None      = None
        self.context: InstanceContext | None  = None
        self.translator: Translator | None    = None
        self.config: TOMLDict | None          = None
        self.dir: pathlib.Path                = None

        self.runtime_config: TOMLDict | None = None

        self.loaded: bool   = False
        self.enabled: bool  = True
        self.failed: bool   = False

        self.commands: dict[str, PluginCommand]  = {}

        self.mod = None

        self.on_install_funcs: list[PluginEventFunction]  = []
        self.on_setup_funcs: list[PluginEventFunction]    = []
        self.on_load_funcs: list[PluginEventFunction]     = []
        self.on_unload_funcs: list[PluginEventFunction]   = []
        self.on_start_funcs: list[PluginEventFunction]    = []

    def fail(self):
        """Marks a plugin as failed and logs an error about plugin fail"""

        self.logger.error('{}', 'Plugin failed')
        self.failed = True

    def is_installed(self) -> bool:
        """Checks for the .installed file in the plugin directory.

        :returns: True if the file is exists, otherwise False"""

        return (self.dir / '.installed').exists()

    def is_disabled(self):
        """Checks for the .disabled file in the plugin directory.

        :returns: True if the file is exists, otherwise False"""

        return (self.dir / '.disabled').exists()

    ####

    def _install(self):
        """Calls all on_install wrappers and marks it installed"""

        try:
            results = []

            for f in self.on_install_funcs:
                results.append(f())

            if all(results):
                # create .installed file and mark this plugin as installed
                (self.dir / '.installed').touch()
            else:
                self.logger.critical('Installation process failed! Plugin is failed')
                self.fail()

        except Exception as e:
            self.logger.error('Exception has been occurred while executing "{}" wrappers', 'on_install')
            self.logger.exception('Exception:', exception=e)

            self.fail()

    def _setup(self):
        """Setups a plugin and calls all on_setup wrappers"""

        self.logger = ezlog.Logger(self.config['name'], group='Plugins')

        self.enabled = not self.is_disabled()
        if not self.enabled:
            return

        if not self.is_installed():
            self._install()

        if self.failed:
            return

        if self.config['debug']['indev']:
            self.logger.warning('Plugin {} in the development mode', self.config["name"])
            self.context.notifies.append(f'Plugin `{self.config["name"]}` in the development mode!')

        try:
            for f in self.on_setup_funcs:
                f()
        except Exception as e:
            self.logger.error('Exception has been occurred while executing "{}" wrappers', 'on_setup')
            self.logger.exception('Exception:', exception=e)

            self.fail()

    def _load(self):
        """Calls all on_load wrappers"""

        if self.failed:
            return

        self.loaded = True

        try:
            for f in self.on_load_funcs:
                f()
        except Exception as e:
            self.logger.error('Exception has been occurred while executing "{}" wrappers', 'on_load')
            self.logger.exception('Exception:', exception=e)

            self.fail()

    def _unload(self):
        """Calls all on_unload wrappers"""

        if self.failed:
            return

        self.loaded = False

        try:
            for f in self.on_unload_funcs:
                f()
        except Exception as e:
            self.logger.error('Exception has been occurred while executing "{}" wrappers', 'on_unload')
            self.logger.exception('Exception:', exception=e)

            self.fail()

    def _start(self):
        """Calls all on_start wrappers"""

        if self.failed:
            return

        try:
            for f in self.on_start_funcs:
                f()
        except Exception as e:
            self.logger.error('Exception has been occurred while executing "{}" wrappers', 'on_start')
            self.logger.exception('Exception:', exception=e)

            self.fail()

    ####

    def on_install(self, func: PluginEventFunction) -> PluginEventFunction:
        """Decorator takes function that be called on plugin installation.
        on_install event checks output of all wrappers to event. If any return False, installation is failed.
        If all on_install event wrappers returned True, then installation is successful and plugin marks as installed.
        """

        self.on_install_funcs.append(func)

        return func

    def on_setup(self, func: PluginEventFunction) -> PluginEventFunction:
        """Decorator takes function that be called on plugin setup"""

        self.on_setup_funcs.append(func)

        return func

    def on_load(self, func: PluginEventFunction) -> PluginEventFunction:
        """Decorator takes function that be called on plugin loads"""

        self.on_load_funcs.append(func)

        return func

    def on_unload(self, func: PluginEventFunction) -> PluginEventFunction:
        """Decorator takes function that be called on plugin unloads"""

        self.on_unload_funcs.append(func)

        return func

    def on_start(self, func: PluginEventFunction) -> PluginEventFunction:
        """Decorator takes function that be called on plugin starts"""

        self.on_start_funcs.append(func)

        return func

    ####

    def register_command(self,
                         function: PluginCommand,
                         names: list[str] | str | None = None,
                         arguments: list[Argument] | ArgumentParser | None = None,
                         permissions: list[str | Permissions] | None = None) -> PluginCommand:
        """Registers a command. You may use :func:`command` decorator to more comfortable

        :param function: Function to register
        :param names: Names of the command
        :param arguments: Arguments of the command
        :param permissions: Permissions for the command
        """

        # initialize names
        if names is None:
            names = [function.__name__]
        else:
            names = names if isinstance(names, list) else [names, ]

        # initialize arguments
        if arguments is None:
            arguments = ArgumentParser(self, [])

        if not isinstance(arguments, ArgumentParser):
            arguments = ArgumentParser(self, arguments)

        # initialize permissions
        if permissions is None:
            permissions = [Permissions.User, f'{self.config["name"]}.{function.__name__}']

        function.permissions  = permissions
        function.parser       = arguments
        function.plugin       = self

        # register command with it names
        for n in names:
            self.commands[n.lower()] = function

        return function

    def remove_command(self, command_names_or_function: str | list[str | PluginCommand] | PluginCommand) -> bool:
        """Removes a command

        :param command_names_or_function: String name of the command or list with the strings or functions or a function

        :returns: True if command deleted successfully, otherwise False
        """

        if isinstance(command_names_or_function, str):
            if command_names_or_function in self.commands and \
                    command_names_or_function in self.context.instance.pluginloader.commands:
                # remove name from the dicts
                self.commands.pop(command_names_or_function)
                self.context.instance.pluginloader.commands.pop(command_names_or_function)

                return True

        elif isinstance(command_names_or_function, list):
            results = []

            for n in command_names_or_function:
                results.append(self.remove_command(n))

            return all(results)

        elif isinstance(command_names_or_function, Coroutine):

            # iterate lists and delete values by key

            for k, v in self.commands.items():
                if v is command_names_or_function:
                    self.commands.pop(k)

            for k, v in self.context.instance.pluginloader.commands:
                if v is command_names_or_function:
                    self.context.instance.pluginloader.commands.pop(k)

        self.logger.debug('Cannot to remove command "{}"', command_names_or_function)

        return False

    ####

    def command(self,
                names: list[str] | str | None = None,
                arguments: list[Argument] | ArgumentParser | None = None,
                permissions: list[str | Permissions] | None = None):
        """Registers a command

        :param names: Names of the command
        :param arguments: Arguments of the command
        :param permissions: Permissions for the command
        """

        def deco(func: PluginCommand) -> PluginCommand:
            return self.register_command(func, names, arguments, permissions)

        return deco
