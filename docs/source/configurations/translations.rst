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

Just copy the file ``en.toml`` in ``lang`` directory and name it as described bottom.

After, you can replace English strings (insert the ``'`` characters) to translated text.

Where is strings?:

.. code-block::

    instance.nonexistent_command  = 'Command isn\'t exists!'
    ---------------------------------^^^^^^^^^^^^^^^^^^^^^^-

.. note:: If your translation contains character ``'``, you must place ``\`` before it.
    Such as ``\'``.

How to name a translation file?
-------------------------------

You must correctly name a file with your translations according to **ISO 639-1**.
Check Wikipedia to get a list of available languages and codes: https://wikipedia.org/wiki/List_of_ISO_639-1_codes

Also, because translation file is ``TOML`` document, you must add ``.toml`` to your file.

Examples: ``en.toml``, ``uk.toml``, ``pl.toml``

Contributing
------------

If you want to provide your translation into framework, then go to
https://github.com/ftdot/ezbotf/issues page, and write an message with `translation` label.

Good luck!
