"""
Contains all to load plugins. The most useful thing is PluginLoader.
"""

import pathlib
import tomllib
import importlib
import importlib.util

from . import ezlog, reprutil
from .context import Context
from .plugin import PluginType, Plugin
from .utils import check_config, load_runtime_config, get_translator_for_plugin, sort_by_priority, update_default_config

from .types import PluginCommand

from typing import Callable

__all__ = ['PluginLoader', 'PluginManageFunction']

# required values for the plugins config
REQUIRED_DEFAULT       = ['name', 'version', 'author', 'description', 'full_description']

# default config of the plugins
default_config = {
    # main sector
    'name':              '-',
    'version':           '-',
    'author':            '-',
    'description':       '-',
    'full_description':  '-',
    'priority':          99,

    # [executable] sector
    'executable': {
        'main_file':   'main.py',
        'main_class':  'plugin',
    },

    # [lang] sector
    'lang': {
        'default':  'en',
        'langs':    ['en'],
    },

    # [requirements] sector
    'requirements': {
        'file':       'requirements.txt',
        'framework':  [],
        'plugins':    [],
    },

    # [debug] sector
    'debug': {
        'indev': False,
    }
}

PluginManageFunction = Callable[[Plugin], None]
PluginManageFunction.__doc__ = 'A type-hint for the functions, that required for :func:`PluginLoader.apply_on_plugins`'


class PluginLoader:
    """Loads and manage all plugins in the given directory

    :ivar plugins_dir: Directory with the plugins
    :ivar translator_lang: Language for the plugin translators
    :ivar plugins: List with the initialized plugins
    :ivar logger: Logger of the PluginLoader
    :ivar plugins_group: Group of logger for the plugins
    :ivar context: Working context
    :ivar commands: Dict with the commands
    """

    def __init__(self, plugins_dir: pathlib.Path, translator_lang: str):
        """
        :param plugins_dir: Directory with the plugins
        :param translator_lang: Language for the plugin translators
        """

        self.plugins_dir      = plugins_dir
        self.translator_lang  = translator_lang

        self.plugins: list[Plugin] = []

        self.logger: ezlog.Logger | None              = None
        self.plugins_group: ezlog.LoggerGroup | None  = None
        self.context: Context | None                  = None

        self.commands: dict[str, PluginCommand] = {}

    ####

    def initialize(self, main_group: ezlog.LoggerGroup, context: Context):
        """Initializes all elements to work (loggers and context link)

        :param main_group: Main logger group for the all loggers (Plugins logger group, PluginsLoader logger)
        :param context: Working context (must be :class:`InstanceContext`)
        """

        self.logger         = ezlog.Logger('PluginsLoader', group=main_group)
        self.plugins_group  = ezlog.LoggerGroup('Plugins', parent=main_group)
        self.context        = context

    ####

    def import_plugin(self, plugin_dir: pathlib.Path, config_path: pathlib.Path) -> Plugin | None:
        """Imports a plugin. Every plugin must have "plugin.toml" configuration file and main executable file.
        Also, there must be two folders: "lang" and "config"

        :param plugin_dir: Directory with the plugin
        :param config_path: Path to the plugin configuration file

        :returns: :class:`Plugin` if it successfully loaded and initialized, otherwise None will be returned
        """

        # load plugin config
        config = tomllib.loads(config_path.read_text(encoding='utf8'))

        # check configuration
        if not check_config(config, REQUIRED_DEFAULT):
            self.logger.error('Plugin by path {} missing some required config fields', str(plugin_dir))
            self.logger.debug('Required fields: {}', REQUIRED_DEFAULT)
            return

        config = update_default_config(
            default_config,
            config
        )

        executable = plugin_dir / config['executable']['main_file']

        # check for the executable
        if not executable.exists():
            executable = executable.with_suffix('.pyc')

            if not executable.exists():
                self.logger.critical('Cannot find executable for plugin {}', config["name"])
                return

        # import plugin
        try:
            mod_spec    = importlib.util.spec_from_file_location(f'Plugin_{config["name"]}',
                                                                 executable
                                                                 )
            plugin_mod  = importlib.util.module_from_spec(mod_spec)
        except Exception as e:
            self.logger.error('Exception has been occurred while loading module of plugin {}', config['name'])
            self.logger.exception('Exception:', exception=e)
            self.logger.debug('May be you passed incorrect main file to the {} in config', 'executable.main_file')
            return

        # try to execute module
        try:
            mod_spec.loader.exec_module(plugin_mod)
        except Exception as e:
            self.logger.error('Exception has been occurred while executing module of plugin {}', config['name'])
            self.logger.exception('Exception:', exception=e)
            return

        # get plugins class
        plugin_class = getattr(plugin_mod, config['executable']['main_class'], None)

        if plugin_class is None:
            self.logger.error('Can\'t import {} class from main file of plugin {}',
                              config['executable']['main_class'],
                              config['name'])
            return

        # setup plugin
        plugin_class.context  = self.context
        plugin_class.mod      = plugin_mod
        plugin_class.config   = config
        plugin_class.dir      = plugin_dir

        return plugin_class

    def initialize_plugins(self):
        """Initializes all plugins in "plugins_dir" directory to `plugins` list"""

        plugins_partial = {}

        # get plugins directories & import it
        for obj in self.plugins_dir.iterdir():
            plugin_config = obj / 'plugin.toml'

            # check for the plugin config
            if obj.is_dir() and plugin_config.is_file():
                plugin = self.import_plugin(obj, plugin_config)

                # register plugin if it is successfully imported
                if plugin is not None:
                    self.logger.info('Plugin {} successfully loaded', plugin.config['name'])

                    self.logger.debug('Begin setup of {} plugin', plugin.config['name'])
                    plugin._setup()

                    self.plugins.append(plugin)

    ####

    def load_plugin(self, plugin: Plugin):
        """Loads a :class:`Plugin`, if it is not failed.
        Loads the runtime config and translator, after calls method :func:`Plugin._load()`
        Also, adds all plugin commands to PluginLoader `commands` dictionary


        :param plugin: :class:`Plugin` to load
        """

        if plugin.failed:
            return

        self.logger.debug('Loading plugin {}', plugin.config['name'])

        plugin.runtime_config  = load_runtime_config(plugin)
        plugin.translator      = get_translator_for_plugin(plugin, self.translator_lang)

        # try to call load method
        try:
            plugin._load()
        except Exception as e:
            self.logger.error('While loading the plugin {} was occurred the exception', plugin.config['name'])
            self.logger.exception('Exception while call "{}" method', 'load()', exception=e)

        # register all plugin commands
        self.commands.update(plugin.commands)

    def unload_plugin(self, plugin: Plugin):
        """Unloads a :class:`Plugin`, if it is not failed.
        Unloads the runtime config and sets translator to None, after calls method :func:`Plugin._unload()`
        Also, deletes all plugin commands from PluginLoader `commands` dictionary

        :param plugin: :class:`Plugin` to unload
        """

        if plugin.failed:
            return

        self.logger.debug('Unloading plugin {}', plugin.config['name'])

        plugin.runtime_config  = None
        plugin.translator      = None

        # try to call unload method
        try:
            plugin._unload()
        except Exception as e:
            self.logger.error('While unloading the plugin {} was occurred the exception', plugin.config['name'])
            self.logger.exception('Exception while call "{}" method', 'unload()', exception=e)

        # remove all commands of the plugin
        for key in plugin.commands:
            self.commands.pop(key)

    def start_plugin(self, plugin: Plugin):
        """Starts a :class:`Plugin`, if it is not failed

        :param plugin: :class:`Plugin` to start
        """

        if plugin.failed:
            return

        self.logger.debug('Starting plugin {}', plugin.config['name'])

        # try to call start method
        try:
            plugin._start()
        except Exception as e:
            self.logger.error('While starting the plugin {} was occurred the exception', plugin.config['name'])
            self.logger.exception('Exception while call "{}" method', 'start()', exception=e)

    def reload_plugin(self, plugin: Plugin):
        """Unloads :class:`Plugin` by :func:`unload_plugin()` method, reloads plugin python executable (re-import) and
        loads back by :func:`load_plugin()` method.
        It is usable for plugin development

        :param plugin: :class:`Plugin` to reload
        """

        self.logger.debug('Reloading plugin {}', plugin.config['name'])

        self.unload_plugin(plugin)

        # reload plugins module
        importlib.reload(plugin.mod)

        self.load_plugin(plugin)

    ####

    def apply_on_plugins(self, action: str, function: PluginManageFunction):
        """Sorts all initialized plugins by Core,Library,Standalone types and priority. After, activates it with function

        :param action: Action that be used there
        :param function: Function to call on each plugin
        """

        corelibrary_plugins  = []
        core_plugins         = []
        library_plugins      = []
        standalone_plugins   = []

        # sort plugins by type

        for p in self.plugins:
            match p.type:
                case PluginType.CoreLibrary:
                    corelibrary_plugins.append(p)
                case PluginType.Core:
                    core_plugins.append(p)
                case PluginType.Library:
                    library_plugins.append(p)
                case PluginType.Standalone:
                    standalone_plugins.append(p)

        corelibrary_plugins  = sort_by_priority(corelibrary_plugins)
        core_plugins         = sort_by_priority(core_plugins)
        library_plugins      = sort_by_priority(library_plugins)
        standalone_plugins   = sort_by_priority(standalone_plugins)

        def apply_function(plugin_list: list[Plugin]):
            for p in plugin_list:
                function(p)

        # apply function on plugins

        self.logger.debug(action, 'CoreLibrary')
        apply_function(corelibrary_plugins)

        self.logger.debug(action, 'Core')
        apply_function(core_plugins)

        self.logger.debug(action, 'Library')
        apply_function(library_plugins)

        self.logger.debug(action, 'Standalone')
        apply_function(standalone_plugins)

    def load_plugins(self):
        """Load all plugins, Shorthand for the apply_on_plugins()"""

        self.apply_on_plugins('Loading {} plugins', self.load_plugin)

    def unload_plugins(self):
        """Unloads all plugins, Shorthand for the apply_on_plugins()"""

        self.apply_on_plugins('Unloading {} plugins', self.unload_plugin)

    def start_plugins(self):
        """Starts all plugins, Shorthand for the apply_on_plugins()"""

        self.apply_on_plugins('Starting {} plugins', self.start_plugin)

    ####

    def get_command(self, command: str) -> PluginCommand | None:
        """Tries to get a command from `commands` dictionary

        :param command: Command name

        :returns: PluginCommand function, if command is exists and parent plugin of command is enabled and not failed.
                  Otherwise, returns None"""
        # check if command is exists
        if command not in self.commands:
            return

        command = self.commands[command]

        # check if plugin of command is enabled and not failed
        if not command.plugin.enabled or command.plugin.failed:
            return

        return command

    ####

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return reprutil.get_repr(self)
