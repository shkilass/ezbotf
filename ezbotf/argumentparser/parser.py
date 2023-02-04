
from . import _casts
from .casts import *
from .argumentparseerror import *

from ..context import Context
from .. import ezlog

from ..types import PluginCommand
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..plugin import Plugin

__all__ = ['Argument', 'ReplyToArgument', 'ArgumentParser']

# symbols to escape
escape_dict = {
    '"': '"',
    "'": "'"
}

# number of messages to iter when reply-to functional is used
RT_ITER_NUM = 50


class Argument:
    """Sample argument"""

    def __init__(self,
                 arg_name: str,
                 arg_type: _casts.ArgTypeCast = Cast.StrCast,
                 default: Any | None = None,
                 description: str = 'Sample argument'
                 ):
        """
        :param arg_name: Name of the argument
        :param arg_type: Type of the argument (NOTE: It must support type-casting with using str)
        :param default: Defines default value of the argument. If it None - argument is marked as required
        :param description: Description of the argument
        """

        self.arg_name = arg_name
        self.arg_type = arg_type
        self.default = default
        self.description = description

        self.is_optional = self.default is not None

    def typecast(self, input_arg: str) -> (bool, Exception | Any):
        """Try to type-cast the string argument to the argument type

        :param input_arg: Input argument in the str type

        :return: Tuple with elements: first is bool (if True then type-casting is return exception, otherwise, if False it is successful), second is type-casted object or Exception (if first is True)
        """

        try:
            return False, self.arg_type.typecast(input_arg) if input_arg != '' else self.default
        except Exception as e:
            return True, e


class ReplyToArgument(Argument):
    """Argument for the Reply-To functional. This is inherits :class:`Argument`"""
    pass

# cache of the ArgumentParser
_CACHED = {}


class ArgumentParser:
    """Helps to manage the arguments

    :ivar parent_plugin: Parent plugin of this parser
    :ivar arguments: List with the arguments
    :ivar allow_caching: Use the caching when it parses the arguments
    :ivar logger: Logger of the argument parser
    :ivar position_arguments: Number of the position arguments
    :ivar default_arguments: Number of the default arguments
    :ivar stack_arguments: Number of the stack arguments
    """

    def __init__(self,
                 parent_plugin: 'Plugin',
                 arguments: list[Argument],
                 allow_caching: bool = True,
                 enable_escaping: bool = False,
                 subcommands: bool = False,
                 main_command_aliases: str | list[str] | None = None,
                 stack_arguments: int = 0
                 ):
        """
        :param parent_plugin: Parent plugin of this parser

        :param arguments: List with the arguments
        :param allow_caching: Use the caching when it parses the arguments
        :param enable_escaping: Enable the escaping by "\" character
        :param subcommands: Enable the subcommands feature
        :param main_command_aliases: Name of the main commands (requires "subcommands")
        :param stack_arguments: Is number of "stack" arguments. This is a positional arguments, that doesn't have name
        """

        self.parent_plugin    = parent_plugin
        self.arguments        = arguments
        self.allow_caching    = allow_caching
        self.enable_escaping  = enable_escaping
        self.subcommands      = subcommands

        self.logger: ezlog.Logger = ezlog.Logger('ArgumentParser')

        self.logger.debug('Initializing the values')
        self.position_arguments: int  = 0
        self.default_arguments: int   = 0
        self.stack_arguments: int     = stack_arguments

        for arg in self.arguments:
            if arg.default:
                self.default_arguments += 1
                continue

            self.position_arguments += 1

        self.subcommands_dict: dict[PluginCommand] = {}

        if self.subcommands:
            # create empty command by the plugin decorator
            self.parent_plugin.command(main_command_aliases, ap=self)(self.parent_plugin.async_empty)

        # check for the reply-to argument
        if len(self.arguments) > 0 and isinstance(self.arguments[0], ReplyToArgument):
            if self.arguments[0].default is None:
                self.position_arguments -= 1

    def _cached_check(self, string: str) -> list[str]:
        """Checker for the cached parsed value

        :param string: String to use

        :return: Executed + new cached result or already cached result of the :func:`parse_string()` method
        """

        if not self.allow_caching:
            return self.parse_string(string)

        # get hash of the string
        str_hash = hash(string)

        if str_hash not in _CACHED:
            _CACHED[str_hash] = self.parse_string(string)

        return _CACHED[str_hash]

    ####

    def parse_string(self, string: str) -> list[str]:
        """Parses the string to the list with the arguments

        :param string: String to parse

        :return: List with the parsed arguments (raw, string type)
        """

        # initialize the variables to first parse stage
        str_open       = False
        str_open_char  = None
        temp_str       = ''
        temp_args      = []
        escaped        = False

        # first parse stage (strings with spaces, escaping)
        for s in string:

            if escaped:
                if s not in escape_dict:
                    # do not escape the character
                    temp_str += '\\' + s
                else:
                    # escape the character to other character in escape dict
                    temp_str += escape_dict[s]

                escaped = False
                continue

            match s:
                case '\\':
                    # check if escaping is enabled
                    if not self.enable_escaping:
                        continue

                    escaped = True

                case "'" | '"':
                    # check if characters is different
                    if str_open_char is not None and str_open_char != s:
                        temp_str += s
                        continue

                    # check for the opened string
                    if str_open:
                        str_open = False
                        str_open_char = None
                    else:
                        str_open = True
                        str_open_char = s

                case ' ':
                    # check for the open string
                    if not str_open:
                        temp_args.append(temp_str)
                        temp_str = ''
                    else:
                        # add space to current string
                        temp_str += ' '

                case '\00':
                    if temp_str != '':
                        temp_args.append(temp_str)

                case _:
                    temp_str += s

        return temp_args

    async def parse(self, text: str, event, command_func: PluginCommand) -> (bool, Context | ArgumentParseError):
        """Parses text (with command) into the arguments

        :param text: Message text with command
        :param event: Telethon event
        :param command_func: Command function to execute

        :return: Tuple with elements: first is bool (True if success, False if result is error), second is :class:`Context` with parsed arguments or :class:`ArgumentParseError` (if first is False)
        """

        self.logger.debug('ArgumentParser called with text: {}', text)

        args = text.split(' ')

        # check for the subcommands
        if self.subcommands:
            self.logger.debug('Command with subcommands has called')

            # check for the arguments length
            if len(args) < 2:
                self.logger.debug('Too little arguments')
                return ArgumentParseError.TooLittleArguments

            # check for the subcommand
            if args[2] in self.subcommands_dict:
                self.logger.debug('Call the subcommand function')

                func = self.subcommands_dict[args[2]]  # get function

                # check for the ArgumentParser is using in command
                if func.ap is not None:
                    return await func.ap.parse([args[0]] + args[2:], event, func)

                self.logger.info('Function {} (command: {}) doesn\'t have ArgumentParser!', func.__name__, args[2])

                return None
            else:
                return ArgumentParseError.IncorrectSubcommand

        # initialize the variables
        output_args = Context()
        output_args.PREFIX = args[0]
        output_args.CMD = args[1]
        temp_args = []

        if len(args) > 2:
            input_str = ' '.join(args[2:]) + '\00'

            # parse the stringuity
            temp_args = self._cached_check(input_str)

        # check for the reply-to argument
        if len(self.arguments) > 0 and isinstance(self.arguments[0], ReplyToArgument):
            arg = self.arguments[0]

            # check if message has reply-to
            if event.reply_to:
                # find reply-to message
                msg = [msg async for msg in
                       self.parent_plugin.context.instance.client.iter_messages(event.chat_id, RT_ITER_NUM)
                       if msg.id == event.reply_to.reply_to_msg_id]
                if len(msg) == 0:
                    return ArgumentParseError.CantFindOriginalMessage
                msg = msg[0]

                # type-cast the argument
                error, result = arg.typecast(msg.message)

                # check for the error
                if error:
                    self.logger.debug('Can\'t cast the argument')
                    log_exception(self.logger, result)

                    return ArgumentParseError.IncorrectType

                # set up the type-casted reply-to message
                setattr(output_args, arg.arg_name, result)
                setattr(output_args, 'REPLY_TO_MESSAGE', msg)
            else:
                if arg.default is None:
                    return ArgumentParseError.ReplyToRequired

        # compare the positional arguments
        if len(temp_args) < self.position_arguments:
            self.logger.debug('Too little arguments')
            return ArgumentParseError.TooLittleArguments

        # compare the arguments sum length
        if len(temp_args) > self.position_arguments + self.default_arguments + self.stack_arguments:
            self.logger.debug('Too much arguments')
            return ArgumentParseError.TooManyArguments

        # initialize the default arguments
        for arg in self.arguments:
            if arg.default:
                setattr(output_args, arg.arg_name, arg.default)

        # type-cast & define the arguments
        for arg, targ in zip(self.arguments, temp_args):
            # type-cast the argument
            error, result = arg.typecast(targ)

            # check for the error
            if error:
                self.logger.debug('Can\'t cast the argument')
                log_exception(self.logger, result)

                return ArgumentParseError.IncorrectType

            # define variable
            setattr(output_args, arg.arg_name, result)

        if self.stack_arguments != 0:
            output_args.STACK = []

            for arg, targ in zip([None]*len(self.arguments) + [0]*self.stack_arguments, temp_args):
            
                # skip argument if it is positional\default
                if arg is None:
                    continue

                output_args.STACK.append(targ)

        # call the command
        try:
            await command_func(event, output_args)

        except Exception as e:
            command_func.plugin.logger.error('While executing command {} occurred an error', output_args.CMD)
            command_func.plugin.logger.exception('Exception:', exception=e)

            return ArgumentParseError.PluginError

        return None

    ####

    def subcommand(self, aliases: str | list | None = None, ap=None):
        """Decorator, that helps register the new subcommand.
           This is redirects to the `parent_plugin.command` decorator

        :param aliases: Aliases to the command
        :param ap: Argument parser

        :return: Function with the changed attributes
        """

        def deco(func: PluginCommand):
            nonlocal aliases

            # register command by the plugins decorator
            func = self.parent_plugin.command(aliases, ap, static_pname)(func)

            # register aliases in the argument parser subcommands dict
            aliases = aliases if isinstance(aliases, list) else [aliases, ]
            for a in aliases:
                self.subcommands_dict[a] = func

            return func

        return deco
