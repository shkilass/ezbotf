"""
Minimal color-supported logging library.
Specially written for the EzBot Framework project

+== Quick start ==
| >>> import ezlog
| >>> import sys
| >>> stdout_handler = ezlog.LoggerHandler(sys.stdout, log_level=ezlog.LogLevel.INFO)
| >>> file_handler = ezlog.LoggerHandler(open('log.txt', 'w'), log_level=ezlog.LogLevel.DEBUG)
| >>> logger = ezlog.Logger('MyLogger', handlers=[stdout_handler, file_handler])
| >>> logger.info('This is an number: {}', 12)
"""

import sys
import typing

import colorama
import traceback

from datetime import datetime
from typing import TextIO, Any, Self

# Fix colors for the windows
if sys.platform == 'win32':
    colorama.just_fix_windows_console()
    colorama.init()


# log levels
class LogLevel:
    """Stores levels of log"""

    DEBUG      = 1
    EXCEPTION  = 2
    INFO       = 5
    WARNING    = 10
    ERROR      = 15
    CRITICAL   = 20
    NOTSET     = 9999


# names of the log levels
level_names = {
    LogLevel.DEBUG:      'DEBUG',
    LogLevel.EXCEPTION:  'EXCEPTION',
    LogLevel.INFO:       'INFO',
    LogLevel.WARNING:    'WARNING',
    LogLevel.ERROR:      'ERROR',
    LogLevel.CRITICAL:   'CRITICAL',
    LogLevel.NOTSET:     'NOTSET'
}

# default color set
DEFAULT_COLOR_SET = {
    'level': {
        LogLevel.DEBUG:      colorama.Fore.LIGHTWHITE_EX,
        LogLevel.EXCEPTION:  colorama.Fore.LIGHTYELLOW_EX,
        LogLevel.INFO:       colorama.Fore.LIGHTCYAN_EX,
        LogLevel.WARNING:    colorama.Fore.YELLOW,
        LogLevel.ERROR:      colorama.Fore.LIGHTRED_EX,
        LogLevel.CRITICAL:   colorama.Fore.RED
    },
    'types': {
        int:          colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT,
        float:        colorama.Fore.LIGHTCYAN_EX,
        bool:         colorama.Fore.YELLOW,
        str:          colorama.Fore.LIGHTMAGENTA_EX + colorama.Style.BRIGHT,
        bytes:        colorama.Fore.LIGHTMAGENTA_EX,
        list:         colorama.Fore.LIGHTYELLOW_EX + colorama.Style.BRIGHT,
        tuple:        colorama.Fore.MAGENTA,
        'exception':  colorama.Fore.LIGHTRED_EX,
        'all':        colorama.Fore.LIGHTGREEN_EX + colorama.Style.BRIGHT
    }
}

# default formatters
DEFAULT_FORMATTER       = '{time} | {level:<18} | {group_name:<18} -> {name:<18} — {message}'
DEFAULT_TIME_FORMATTER  = '{year:04d}.{month:02d}.{day:02d} {hour:02d}:{minute:02d}:{second:02d}.{microsecond:04s}'

# logger groups
LOGGER_GROUPS = {}

# colors reset
reset = colorama.Style.RESET_ALL


# utilities

def level_to_color(level: int, color_set: dict) -> str:
    """Converts log level to color

    :param level: Int level to convert
    :param color_set: Color set from get the colors

    :returns: String color of the level if level is registered, otherwise empty string
    """

    if level in color_set['level']:
        return color_set['level'][level]

    return ''


def level_to_name(level: int) -> str:
    """Converts log level to str

    :param level: Level to convert

    :returns: Level as string or empty string if level is not registered
    """

    if level in level_names:
        return level_names[level]

    return ''


def type_to_color(type_: type | str, color_set: dict) -> str:
    """Converts type to the color

    :param type_: Type to convert
    :param color_set: Color set from get colors of the types

    :returns: String with color of the type or returns color_set['types']['all'] color
    """

    if type_ in color_set['types']:
        return color_set['types'][type_]

    return color_set['types']['all']


def register_log_level(level: int, level_name: str):
    """Registers new log level

    :param level: Int level to register
    :param level_name: Name of the level to register
    """

    setattr(LogLevel, level_name, level)
    level_names[level] = level_name


def make_logger_binding(level: int) -> ...:
    """Makes function bind to do record for the given log level

    :param level: Int level to bind

    :returns: Bind function to log the given log level
    """

    def f(self, message: str, *args, exception: Exception | None = None):
        if level == LogLevel.CRITICAL:
            message = f'{colorama.Back.LIGHTRED_EX}{message}{colorama.Style.RESET_ALL}'

        self.record(message, *args, level=level, exception=exception)

    return f


def register_bindings(cls):
    """Registers bindings for the levels to a Logger class

    :param cls: Class (must be Logger class)
    :type cls: Logger
    """

    # make bindings to the all log levels
    for level, name in level_names.items():
        name_l = name.lower()

        if getattr(cls, name_l, None) is not None:
            continue

        setattr(cls, name.lower(), make_logger_binding(level))


class LoggerHandler:
    """Handler for any IO"""

    def __init__(self: Self,
                 io: TextIO | None = None,
                 log_level: int = LogLevel.NOTSET,
                 colors: bool = True,
                 exceptions: bool = True):
        """
        :param io: TextIO to handle
        :param log_level: Level of logs (by default is LogLevel.NOTSET)
        :param colors: Enable colors for the logger
        """

        self.io          = io
        self.log_level   = log_level
        self.colors      = colors
        self.exceptions  = exceptions

    def write(self: Self, text: str):
        """Writes given text to the IO if it doesn't equals to None

        :param text: Text to write into IO
        """
        if self.io is None:
            return

        self.io.write(text)
        self.io.flush()


class LoggerGroup:
    """Group of loggers has shared parameters.
       Is highly recommended to create root logger and after pin all others logger to it
    """

    def __init__(self: Self,
                 name: str,
                 parent=None,
                 formatter: str | None = None,
                 time_formatter: str | None = None,
                 color_set: dict[str, dict[type | str, str]] | None = None,
                 handlers: list[LoggerHandler] | None = None,
                 loggers: list | None = None
                 ):
        """

        :param name: Name of the group
        :param parent: Parent of this group
        :type parent: LoggerGroup
        :param formatter: Formatter for the logs
        :param time_formatter: Formatter for the time
        :param color_set: Set of the colors to use
        :param handlers: Handlers, used to write all logs into
        """
        self.name = name

        if parent is None:
            self.formatter       = formatter if formatter is not None else DEFAULT_FORMATTER
            self.time_formatter  = time_formatter if time_formatter is not None else DEFAULT_TIME_FORMATTER
            self.color_set       = color_set if color_set is not None else DEFAULT_COLOR_SET
            self.handlers        = handlers if handlers is not None else []

        else:

            if isinstance(parent, str):
                parent = LOGGER_GROUPS[parent]

            self.formatter       = parent.formatter
            self.time_formatter  = parent.time_formatter
            self.color_set       = parent.color_set
            self.handlers        = parent.handlers

        if isinstance(loggers, list):
            self.loggers = loggers

            # initialize all loggers
            for logger in self.loggers:
                logger.group = self
                logger.initialize_group()

        LOGGER_GROUPS[name] = self


class Logger:
    """Class of the Logger"""

    def __init__(self: Self,
                 name: str,
                 formatter: str | None = None,
                 time_formatter: str | None = None,
                 color_set: dict[str, dict[type | str, str]] | None = None,
                 handlers: list[LoggerHandler] | None = None,
                 group: LoggerGroup | str | None = None
                 ):
        """
        :param name: Name of the logger
        :param formatter: String formatter of the record
        :param time_formatter: String formatter for the time
        :param color_set: Colors set to use (dict with the colors)
        :param handlers: Handlers (List with the LoggerHandler instances). It is using to write records in
        :param group: Group of the handler (Copy all values from)
        """

        self.name = name

        if group is not None:
            # copy settings from the logger group

            if isinstance(group, str):
                group = LOGGER_GROUPS[group]

            self.group = group

            self.initialize_group()

        else:

            # register logger settings
            self.formatter       = formatter if formatter is not None else DEFAULT_FORMATTER
            self.time_formatter  = time_formatter if time_formatter is not None else DEFAULT_TIME_FORMATTER
            self.color_set       = color_set if color_set is not None else DEFAULT_COLOR_SET
            self.handlers        = handlers if handlers is not None else []

            self.group           = None

    def initialize_group(self: Self):
        """Copy all settings from group to itself"""

        self.formatter       = self.group.formatter
        self.time_formatter  = self.group.time_formatter
        self.color_set       = self.group.color_set
        self.handlers        = self.group.handlers

    def format_time(self: Self, time: datetime) -> str:
        """Formats a time with time_formatter attribute

        :param time: Time to format

        :returns: Formatted time
        """

        return self.time_formatter.format(year=time.year,
                                          month=time.month,
                                          day=time.day,
                                          hour=time.hour,
                                          minute=time.minute,
                                          second=time.second,
                                          microsecond=str(time.microsecond)[:4])

    def format_message(self: Self, message: str, args_str: list[str], level_str: str, time_str: str) -> str:
        """Formats given message with formatter attribute

        :param message: Message to format
        :param args_str: Arguments to format the message
        :param level_str: Level parameter
        :param time_str: Time parameter
        """

        return self.formatter.format(message=message.format(*args_str),
                                     time=time_str,
                                     name=self.name,
                                     group_name=self.group.name if self.group is not None else 'NoGroup',
                                     level=level_str,
                                     color=colorama.Fore,
                                     reset=reset
                                     )

    def record(self: Self, message: str, *args: Any, level: int = LogLevel.NOTSET, exception: Exception | None = None):
        """Records a log to the handlers with using formatters

        :param message: Message to record
        :param args: Arguments to format with message
        :param level: Log level of the record
        :param exception: Exception (if haven) to log
        """

        # get formatted time
        time_str = self.format_time(datetime.now())

        # get colored args\text
        args_str     = [str(o) for o in args]
        args_colored = [type_to_color(type(o), self.color_set) + str(o) + reset for o in args]

        level_str      = level_to_name(level)
        level_colored  = level_to_color(level, self.color_set) + level_str + reset

        # get formatted message
        f_message            = self.format_message(message, args_str, level_str, time_str)
        f_message_colored    = self.format_message(message, args_colored, level_colored, time_str)

        # write record to the handlers
        for h in self.handlers:
            if h.log_level <= level:
                h.write((f_message_colored if h.colors else f_message) + '\n')

                if exception:
                    # get color for the exception (if handler is supports colors)
                    exception_color = type_to_color('exception', self.color_set)

                    h.write(exception_color + ''.join(traceback.format_exception(exception)).removeprefix('\n') + reset + '\n')

# register bindings
register_bindings(Logger)
