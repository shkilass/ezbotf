"""
Here is defined a bot instance. This class managing all framework elements in one.
If you not an advanced developer, you may use an **ezbotf-cli**.
To get help about it, you must type in your terminal:
# ezbotf -h
"""

import pathlib
import tomlkit
import sys

import asyncio
import nest_asyncio

from telethon import TelegramClient, events
from telethon.events.raw import EventBuilder

from datetime import datetime

from . import ezlog, utils, messages, version, reprutil
from .argumentparser import ArgumentParseError
from .pluginloader import PluginLoader
from .instancecontext import InstanceContext, DirsContext
from .exceptions import IncorrectInstanceConfigError
from .translator import Translator
from .permissions import Permissions
from .messages import prefixes_dict

from .types import TOMLDict, PermissionsDict
from typing import Any

nest_asyncio.apply()

__all__ = ['BotInstance']


# required config values
REQUIRED_DEFAULT          = ['name', 'prefixes', 'language', 'api_id', 'api_hash',
                             'dirs', 'logging', 'warnings']
REQUIRED_DIRS             = ['plugins_dir', 'cache_dir', 'logs_dir', 'lang_dir']
REQUIRED_LOGGING          = ['console_log_level', 'file_log_level']
REQUIRED_WARNINGS         = ['ignore_nonexistent_command', 'ignore_plugin_errors']

REQUIRED_CONFIG = {
    'dirs': REQUIRED_DIRS,
    'logging': REQUIRED_LOGGING,
    'warnings': REQUIRED_WARNINGS
}


class BotInstance:
    """Instance of the bot

    :ivar config: TOML config of instance
    :ivar logger: Logger of instance
    :ivar main_group: Main logger group of instance. All loggers will be use it as parent
    """

    def __init__(self, config: TOMLDict | None = None):
        """
        :param config: Preloaded TOML dict config to use. If it not set, you must use :func:`import_config()` method
        """

        self.config = config

        self.logger: ezlog.Logger | None           = None
        self.main_group: ezlog.LoggerGroup | None  = None

        self.pluginloader: PluginLoader | None     = None
        self.context: InstanceContext | None       = None
        self.client: TelegramClient | None         = None
        self.translator: Translator | None         = None
        self.permissions: PermissionsDict | None   = None

        self.prefixes: list[str] = []

    def import_config(self, path: pathlib.Path):
        """Imports a TOML config from path to instance

        :param path: Path to the config

        :raises IncorrectInstanceConfigError: When config is not have required parameters
        """

        self.config = tomlkit.loads(path.read_text(encoding='utf8'))

        if not utils.check_config(self.config, REQUIRED_DEFAULT) or not utils.check_config_by_path(self.config, REQUIRED_CONFIG):
            print(f'ezbotf: Required values as default: {", ".join(REQUIRED_DEFAULT)}')
            raise IncorrectInstanceConfigError(str(path))

    ####

    def setup_context(self):
        """Setups a context attribute that shared between ezbot framework elements and plugins"""

        self.context.instance   = self
        self.context.cache_dir  = pathlib.Path(self.config['dirs']['cache_dir'])
        self.context.notifies   = []
        self.context.owner      = None

        # setup directories
        self.context.dirs                  = DirsContext()
        self.context.dirs.plugins_dir      = pathlib.Path(self.config['dirs']['plugins_dir'])
        self.context.dirs.lang_dir         = pathlib.Path(self.config['dirs']['lang_dir'])
        self.context.dirs.permissions_dir  = pathlib.Path(self.config['dirs']['permissions_dir'])
        self.context.dirs.cache_dir        = pathlib.Path(self.config['dirs']['cache_dir'])
        self.context.dirs.logs_dir         = pathlib.Path(self.config['dirs']['logs_dir'])

    def initialize(self, parent_logger_group: ezlog.LoggerGroup | str | None = None):
        """Initializes all values in instance, such as :class:`PluginLoader`, working context, :class:`Logger` and other

        :param parent_logger_group: Parent logger of this instance
        """

        # setup context
        self.context = InstanceContext()
        self.setup_context()

        # check for the parent logger group
        if parent_logger_group is None:
            log_fn = ezlog.Logger('',
                                  time_formatter=self.config['logging']['time_format'])\
                         .format_time(datetime.now()) + '.log'

            stdout_handler  = ezlog.LoggerHandler(sys.stdout, log_level=self.config['logging']['console_log_level'])
            file_handler    = ezlog.LoggerHandler(
                open(self.context.dirs.logs_dir / log_fn, 'w'),
                log_level=self.config['logging']['file_log_level'],
                colors=False)

            # create own logger group
            parent_logger_group = ezlog.LoggerGroup(self.config['name'], handlers=[stdout_handler, file_handler])

        # initialize all
        self.main_group    = parent_logger_group
        self.logger        = ezlog.Logger('BotInstance', group=self.main_group)
        self.pluginloader  = PluginLoader(self.context.dirs.plugins_dir, self.config['language'])
        self.client        = TelegramClient(self.config['name'], self.config['api_id'], self.config['api_hash'])
        self.translator    = Translator(self.context.dirs.lang_dir, self.main_group, desired_lang=self.config['language'])
        self.permissions   = utils.load_permissions(self.context.dirs.permissions_dir,
                                                    self.config['name'])

        # add prefixes from translation
        if 'prefixes' in self.translator.translations:
            self.prefixes += self.translator.translations['prefixes']

        # add prefixes from config
        self.prefixes += self.config['prefixes']

        # initialize the PluginLoader and initialize plugins
        self.pluginloader.initialize(self.main_group, self.context)
        self.pluginloader.initialize_plugins()

        # register events
        self.client.add_event_handler(self.handle_message, events.NewMessage)
        self.client.add_event_handler(self.handle_message, events.MessageEdited)

        self.logger.info('Instance initialized')
        self.logger.info('Running on version {}', version.ezbotf_version_string_full)

        if version.VersionLabel.InDevelopment in version.ezbotf_labels:
            self.logger.warning('Is running on {} version', version.VersionLabel.InDevelopment)
            self.context.notifies.append(f'{prefixes_dict["warning"]} Version **{version.ezbotf_version_string_full}** of'
                                         ' `EzBot Framework` in the development. Some functions may behave incorrectly')

        # check if current release have unstable label
        if version.VersionLabel.Unstable in version.ezbotf_labels:
            self.logger.warning('Is running on {} version. This may cause problems!', version.VersionLabel.Unstable)
            self.context.notifies.append(f'{prefixes_dict["warning"]} Version **{version.ezbotf_version_string_full}** of'
                                         ' `EzBot Framework` is unstable. This may cause problems!')

    ####

    def load(self):
        """Loads all required items (such as :class:`PluginLoader` and :class:`TelegramClient`)"""

        self.pluginloader.load_plugins()
        self.client.start()

        if not utils.run_coroutine_without_await(self.client.is_user_authorized()):
            self.logger.critical('User isn\'t authorized! Can\'t continue, exiting...')
            exit()

        # get id of instance owner
        self.context.owner                       = utils.run_coroutine_without_await(self.client.get_me())
        self.permissions[self.context.owner.id]  = [Permissions.Owner]

    def run(self):
        """Runs an instance"""

        self.pluginloader.start_plugins()

        # print information about current user
        self.logger.info('{} by user @{}, {} {} [{}]', 'Instance is running',
                         self.context.owner.username,
                         self.context.owner.first_name,
                         self.context.owner.last_name or 'Hasn\'t last name',
                         utils.mask_phone_number(self.context.owner.phone))

        self.client.run_until_disconnected()

    ####

    def quick_run(self):
        """Calls all required methods to start the instance (before using it, you must use :func:`import_config()` method).
           Shorthand for the :func:`initialize()`, :func:`load()`, :func:`run()` methods"""

        self.initialize()
        self.load()
        self.run()

    ####

    async def handle_message(self, event: EventBuilder):
        """Handles a message (Parses and search for the commands)

        :param event: Event of the message from Telethon
        """

        # check if message is have text
        if not (len(event.text) > 0):
            return

        # split message
        args = event.text.split(' ')

        if not len(args) > 1:
            return

        # check for the prefixes
        if not any([p in args[0] for p in self.prefixes]):
            return

        # check for the notifies
        if len(self.context.notifies) != 0:
            await messages.notify(event, self.context.notifies)
            self.context.notifies.clear()

        # get command
        command = self.pluginloader.get_command(args[1])

        if command is None:
            # if command is not found
            self.logger.debug('No command with name {}', args[1])

            if not self.config['warnings']['ignore_nonexistent_command']:
                await event.reply(self.translator.translations['instance']['nonexistent_command'])

            return

        # check permissions
        if not utils.have_permissions((sender := await event.get_sender()).id, self.permissions, command.permissions):
            self.logger.warning('Attempted to run command: {} by @{} (access disallowed)', event.text, sender.username)

            if not self.config['warnings']['ignore_disallow_access']:
                await event.reply(self.translator.translations['instance']['disallow_access'])

            return

        # try to parse arguments and execute the command
        error = await command.parser.parse(event.text, event, command)

        if error:
            match error:
                case ArgumentParseError.TooLittleArguments:
                    await event.respond(self.translator.translations['argumentparser']['too_little_arguments'])

                case ArgumentParseError.TooManyArguments:
                    await event.respond(self.translator.translations['argumentparser']['too_many_arguments'])

                case ArgumentParseError.ReplyToRequired:
                    await event.respond(self.translator.translations['argumentparser']['reply_to_required'])

                case ArgumentParseError.IncorrectType:
                    await event.respond(self.translator.translations['argumentparser']['incorrect_type'])

                case ArgumentParseError.IncorrectSubcommand:
                    await event.respond(self.translator.translations['argumentparser']['incorrect_subcommand'])

                case ArgumentParseError.CantFindOriginalMessage:
                    await event.respond(self.translator.translations['argumentparser']['cant_find_original_message'])

                case ArgumentParseError.PluginError:
                    await event.respond(self.translator.translations['argumentparser']['plugin_error'])

    ####

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return reprutil.get_repr(self)
