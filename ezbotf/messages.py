"""
Contains
"""

from telethon.events.raw import EventBuilder

__all__ = ['prefixes_dict', 'prefixed_message', 'notify', 'success', 'unsuccess', 'blocked', 'warning',
           'important', 'very_important', 'radioactive', 'info', 'question']


# dict with all prefixes for message formatters
prefixes_dict = {
    'notify': '🔔',
    'success': '✅',
    'unsuccess': '❌',
    'blocked': '🚫',
    'warning': '⚠️',
    'important': '❗️',
    'very_important': '‼️',
    'radioactive': '☢️',
    'info': '❕',
    'question': '❔'
}


# function for all message formatters
async def prefixed_message(prefix: str, event: EventBuilder, message: str | list[str]):
    """Formats message(s) with prefix and send it via event (from Telethon)

    :param prefix: Prefix of the message
    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    if isinstance(message, list):
        for msg in message:
            await notify(event, msg)

        return

    await event.respond(f'{prefix} {message}')


async def notify(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as notify. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['notify'], event, message)


async def success(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as success. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['success'], event, message)


async def unsuccess(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as unsuccess. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['unsuccess'], event, message)


async def blocked(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as blocked. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['blocked'], event, message)


async def warning(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as warning. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['warning'], event, message)


async def important(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as important. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['important'], event, message)


async def very_important(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as very important. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['very_important'], event, message)


async def radioactive(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as radioactive. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['radioactive'], event, message)


async def info(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as info. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['info'], event, message)


async def question(event: EventBuilder, message: str | list[str]):
    """Formats message(s) as question. Shorthand for the prefixed_message()

    :param event: Event from Telethon
    :param message: Message(s) to format and send
    """

    await prefixed_message(prefixes_dict['question'], event, message)
