.. _plugin:

.. currentmodule:: ezbotf

=============
plugin module
=============

.. note:: This module is imports as ``from .. import *``. This means that there
    is no need to import it separately or use ``ezbotf.plugin.Plugin``.
    You can simply use ``ezbotf.Plugin`` as example.

There is defined one of main classes - :class:`Plugin`.
This module is contains all required to write a plugin.

There is example of a standalone plugin:

.. code-block:: python

    import ezbotf

    plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)

    @plugin.on_load
    def on_load():

        @plugin.command('example')
        async def example(event, args):
            await ezbotf.messages.info(event, 'This is an example')

.. note:: You must follow **plugin developing guide**, check :ref:`Quick start <plugindev-quickstart>`

PluginType
==========

Enum with possible types of the plugin.

.. autoclass:: PluginType

Plugin
======

.. warning:: Examples there does not use translations system. This is only examples.
    In real cases, recommended to use translation system! Also, these examples doesn't
    use permissions system. Of course, in real cases, you must use it!

.. autoclass:: Plugin

    .. automethod:: __init__

    .. automethod:: fail

    .. automethod:: is_installed

    .. automethod:: is_disabled

    .. automethod:: _install

    .. automethod:: _setup

    .. automethod:: _load

    .. automethod:: _unload

    .. automethod:: _start

    .. automethod:: on_install

        .. note:: This event called only once, when plugin is installing. After installation, plugin
            marks as installed, and on_install event never be called.

        Example:

        Plugin config "plugin.toml":

        .. code-block:: toml

            name     = 'ExampleRequirements'  # name of the plugin
            version  = '1.0.0'                # version of the plugin
            author   = 'ftdot'                # paste here your name

            description       = 'Test requirements'  # small description of the plugin

            # full description of the plugin (you may describe plugin in details)
            full_description  = 'This is the test only plugin. There no big functional'

            [executable]
            main_file   = 'main.py'  # file with the main plugin class
            main_class  = 'plugin'   # name of the plugin instance

            [lang]
            default  = 'en'      # default language of the plugin
            langs    = [ 'en' ]  # supported languages

            [requirements]
            file = 'requirements.txt'
            framework = []
            plugins = [['ExampleLib', ['>=', '1.0.0'], ['<=', '1.0.1']]]

        .. note:: To get code of required **ExampleLib** plugin, see bottom (in :func:`on_load`
            example)

        Plugin "requirements.txt":

        .. code-block::

            prettytable

        Plugin executable "main.py":

        .. code-block:: python

            import ezbotf

            plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)

            @plugin.on_install
            def install_requirements():
                return ezbotf.utils.install_requirements(plugin)

            @plugin.on_install
            def check_required_plugins():
                return ezbotf.utils.check_required_plugins(plugin)

            @plugin.on_load
            def on_load():

                from prettytable import PrettyTable  # you must import your requirements inside on_load event!

                @plugin.command('test')
                async def test(event, args):

                    # check if examplelib is exists in working context
                    if 'examplelib' not in dir(plugin.context):
                        await ezbotf.message.error(event, 'To this plugin is work required `ExampleLib` library!')
                        return

                    # Example table
                    x = PrettyTable()
                    x.field_names = ['Num 1', 'Num 2', 'Operation', 'Result']
                    x.add_row((1, 1, '+', 2))
                    x.add_row((1, 2, '*', 2))
                    x.add_row((20, 5, '/', 4))

                    await plugin.context.examplelib.example(event)  # Call function of our example library
                    await event.respond(str(x))                     # Send example table

        Plugin directory hierarchy must be view as:

        .. code-block::

            examplerequirements/
            |- config/
            |  |- default.toml
            |
            |- lang/
            |  |- en.toml
            |
            |- requirements.txt
            |- main.py
            |- plugin.toml

        .. seealso:: :func:`ezbotf.utils.install_requirements()` and :func:`ezbotf.utils.check_required_plugins()`

    .. automethod:: on_setup

        .. note:: Called only once, when plugin is initializing

        .. warning:: This event is not recommended to use as "on load" to initialize all variables.
            Use :func:`on_load` instead of.

    .. automethod:: on_load

        .. note:: This event called when plugin is loading. It recommended to declare all working
            variables there. But, do not forget delete them in :func:`on_unload` event.
            Also, plugins must declare there all commands.

        Example:

        Plugin config "plugin.toml":

        .. code-block:: toml

            name     = 'ExampleLib'   # name of the plugin
            version  = '1.0.0'        # version of the plugin
            author   = 'ftdot'        # paste here your name

            description       = 'Provides example function'  # small description of the plugin

            # full description of the plugin (you may describe plugin in details)
            full_description  = 'This is example library plugin for EzBotF. This is provides an example function, that deletes message from event'

            [executable]
            main_file   = 'main.py'  # file with the main plugin class
            main_class  = 'plugin'   # name of the plugin instance

            [lang]
            default  = 'en'      # default language of the plugin
            langs    = [ 'en' ]  # supported languages

        Plugin executable "main.py":

        .. code-block:: python

            import ezbotf

            plugin = ezbotf.Plugin(ezbotf.PluginType.Library)

            @plugin.on_load
            def on_load():

                async def example(event):
                    """Example library function, that deletes message from event,
                    that given to it command. Must be awaited!

                    :param event: Event from get message to delete
                    """

                    await event.message.delete()

                plugin.context.examplelib = Context()        # Create new context for our library
                plugin.context.examplelib.example = example  # Link my_lib.example to example function

            @plugin.on_unload
            def on_unload():
                # About on_unload event see bottom

                # Don't forget to delete our library context
                del plugin.context.examplelib

    .. automethod:: on_unload

        .. note:: This event is called when plugin is unloading. You must delete all plugin things,
            such as library contexts, working variables and etc. that defined in :func:`on_load` event.

        .. note:: You isn't required to delete all commands in this event. When plugin is unloaded,
            all commands automatically disables.

        For examples you can view :func:`on_load`.

    .. automethod:: on_start

        .. note:: This event is called only once, when bot instance is start. You can use
            ``context.instance.client`` (:class:`TelegramClient`, from Telethon, see https://docs.telethon.dev/
            for more information about it). But note, that telethon is async library, and you must use
            :func:``ezbotf.utils.run_coroutine_without_await()`` to run coroutines outside of event loop.

    .. automethod:: register_command

    .. automethod:: remove_command

    .. automethod:: command

        Example:

        .. code-block:: python

            import ezbotf

            plugin = ezbotf.Plugin(ezbotf.PluginType.Standalone)

            @plugin.on_load
            def on_load():

                @plugin.command('sum',  # name of command
                                [argumentparser.Argument('num1', argumentparser.Cast.FloatCast),  # Arguments
                                 argumentparser.Argument('num2', argumentparser.Cast.FloatCast)]
                                ['myplugin.test',    # Permissions
                                 Permissions.User])
                async def test(event, args):
                    await event.respond(event, str(args.num1 + args.num2))
