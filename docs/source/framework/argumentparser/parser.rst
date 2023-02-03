.. _argumentparser-parser:

.. currentmodule:: ezbotf.argumentparser

=============
parser module
=============

.. note:: This module is imports as ``from .. import *``. This means that there
    is no need to import it separately or use ``ezbotf.argumentparser.parser.Argument``.
    You can simply use ``ezbotf.argumentparser.Argumentparser`` as example.

Argument
========

.. autoclass:: Argument

    .. automethod:: __init__

    .. automethod:: typecast

ReplyToArgument
===============

.. autoclass:: ReplyToArgument

    .. automethod:: __init__

    .. automethod:: typecast

ArgumentParser
==============

.. autoclass:: ArgumentParser

    .. automethod:: __init__

    .. automethod:: _cached_check

    .. automethod:: parse_string

    .. automethod:: parse

    .. automethod:: subcommand

    Example standalone plugin with ArgumentParser usage:

    .. code-block:: python

        import ezbotf

        plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)

        @plugin.on_load
        def on_load():

            @plugin.command('lowercase',
                            [ezbotf.argumentparser.ReplyToArgument('rt_text', default='<notset>'),
                             ezbotf.argumentparser.Argument('text', default='<notset>')])
            async def lowercase(event, args):
                if args.rt_text == '<notset>' and args.text == '<notset>':
                    await ezbotf.messages.error(event, 'You must reply to any message or write text as first argument')

                text = args.text if args.text != '<notset>' else args.rt_text

                await event.respond(text.lowercase())

    Example standalone plugin with ArgumentParser subcommands usage:

    .. code-block:: python

        import ezbotf

        plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)

        @plugin.on_load
        def on_load():

            # Define Argument Parser with subcommands
            text_operations_ap = ezbotf.ArgumentParser(
                plugin,
                [],
                subcommands=True,
                main_command_aliases='text'
            )

            # Because there is lowercase, uppercase is using the same argument scheme, there is created shared variable for arguments
            shared_text_ops_args = [ezbotf.argumentparser.ReplyToArgument('rt_text', default='<notset>'),
                                    ezbotf.argumentparser.Argument('text', default='<notset>')]

            @text_operations_ap.subcommand('lowercase',
                                           shared_text_ops_args)
            async def text_lowercase(event, args):
                if args.rt_text == '<notset>' and args.text == '<notset>':
                    await ezbotf.messages.error(event, 'You must reply to any message or write text as first argument')

                text = args.text if args.text != '<notset>' else args.rt_text

                await event.respond(text.lowercase())

            @text_operations_ap.subcommand('uppercase',
                                           shared_text_ops_args)
            async def text_lowercase(event, args):
                if args.rt_text == '<notset>' and args.text == '<notset>':
                    await ezbotf.messages.error(event, 'You must reply to any message or write text as first argument')

                text = args.text if args.text != '<notset>' else args.rt_text

                await event.respond(text.uppercase())