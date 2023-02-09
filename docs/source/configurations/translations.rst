.. _translations:

============
Translations
============

There is described, how you can quickly translate the framework. Translations
are use ``TOML`` - powerful language for configurations.

There is example of translation file (English translation):

.. code-block:: toml

    # Translations of the ezbotf Instance
    instance.nonexistent_command  = 'Command isn\'t exists!'
    instance.disallow_access      = 'You have not access to this command!'

    # Translations of the ezbotf ArgumentParser
    argumentparser.too_little_arguments        = 'There is too litle arguments'
    argumentparser.too_many_arguments          = 'There is too many arguments'
    argumentparser.reply_to_required           = 'To use this command, you must reply to any message'
    argumentparser.incorrect_type              = 'Incorrect type of argument'
    argumentparser.incorrect_subcommand        = 'There is no that subcommand'
    argumentparser.cant_find_original_message  = 'Cant find original message from reply to. Limit of distance is 50 messages'
    argumentparser.plugin_error                = 'Plugin returned an exception. You may check the console (if log level if exception+) for the error'

How to start translate?
-----------------------

Just copy file ``en.toml`` in ``lang`` directory and name it as described bottom (**How to name a translation file**)

After, you can replace English strings (insert into the ``'`` characters) to the translated text.

Where is strings?:

.. code-block::

    instance.nonexistent_command = "Command isn't exists!"
    --------------------------------^^^^^^^^^^^^^^^^^^^^^-

If your translated text contains ``'``, then replace ``'`` to ``"``, example:

.. code-block::

    instance.nonexistent_command = "Command isn't exists!"
    -------------------------------^---------------------^

If your translated text contains ``\n``, ``\t`` or other escape character,
you **MUST** use ``"`` for your string.

.. code-block::

    unknown_code = "`CoreLib` function returned unknown code `{}`.\n\nYou may open issue about it: https://github.com/ftdot/ezbotf/issues"
    ---------------^----------------------------------------------^^^^-------------------------------------------------------------------^

.. note:: For newline use ``\n``. For tab character use ``\t``. To use ``"``
    inside ``"``-strings, use ``\"``.

How to name a translation file?
-------------------------------

You must correctly name a file with your translations according to **ISO 639-1**.
Check Wikipedia to get a list of available languages and codes of it: https://wikipedia.org/wiki/List_of_ISO_639-1_codes

Also, because translation file is ``TOML`` document, you must add ``.toml`` to end of your file.

Examples: ``en.toml``, ``uk.toml``, ``pl.toml``

How set instance to other language?
-----------------------------------

In your environment open folder named as ``instances/``. Open instance you required to edit.
As example - ``default.toml`` is ``default`` instance.

After you open your instance, replace this string:

.. code-block:: toml

    ...
    language  = 'en'
    -------------^^-
    ...

With language you want to use. But, this language must be exists in ``lang/`` directory of
your environment! As default, there is only ``en`` (English) translation.

.. seealso:: Codes of languages in **ISO 639-1** format: https://wikipedia.org/wiki/List_of_ISO_639-1_codes

Contributing
------------

.. note:: All default translations of the framework stores in ``ezbotf/env_default/lang/``.

If you want to provide your translation into framework, then:

#. Fork EzBotF repository.
#. Create new branch and name it with your feature. Example: `ru-translation`
#. Commit your changes (as example, add Ukrainian translation).
#. Create pull request and summary of your changes.

Good luck!
