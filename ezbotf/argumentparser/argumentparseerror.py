
from enum import Enum, auto

__all__ = ['ArgumentParseError']


class ArgumentParseError(Enum):
    """Enum with the possible Argument Parser errors

    :ivar TooManyArguments: Returned when to argument parser is passed too many arguments
    :ivar TooLittleArguments: Returned when to argument parser is passed too little arguments
    :ivar IncorrectType: Returned when argument cannot be type-casted
    :ivar IncorrectSubcommand: Returned when to argument parser with subcommands passed nonexistent subcommand
    :ivar ReplyToRequired: Returned when required to reply to any message to work with command
    :ivar CantFindOriginalMessage: Returned when limit of messages distance is reached and message doesn't found
    :ivar PluginError: Returned when plugin raised an exception
    """

    TooManyArguments         = auto()
    TooLittleArguments       = auto()
    IncorrectType            = auto()
    IncorrectSubcommand      = auto()
    ReplyToRequired          = auto()
    CantFindOriginalMessage  = auto()
    PluginError              = auto()
