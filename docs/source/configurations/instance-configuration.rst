.. _instance-configuration:

======================
Instance configuration
======================

Instance configuration is a file, that defines all required configurations, such as
directory to the plugin, logging level, instance name, and other.

Example configuration
---------------------

Example configuration view as:

.. code-block:: toml

    name      = 'DefaultInstance'
    prefixes  = ['ez', 'easy', 'изи', 'ізі']
    language  = 'en'

    api_id    = -1
    api_hash  = ''

    [dirs]
    plugins_dir     = './plugins/'
    cache_dir       = './cache/'
    logs_dir        = './logs'
    lang_dir        = './lang/'
    permissins_dir  = './permissions/'

    [logging]
    # Log levels:
    #    DEBUG      = 1
    #    EXCEPTION  = 2
    #    INFO       = 5
    #    WARNING    = 10
    #    ERROR      = 15
    #    CRITICAL   = 20

    console_log_level  = 2  # EXCEPTION
    file_log_level     = 1  # DEBUG

    # format of the time for name of the log file
    time_format = '{year:04d}.{month:02d}.{day:02d}_{hour:02d}_{minute:02d}_{second:02d}.{microsecond:04s}'

    [warnings]
    ignore_nonexistent_command  = true   # if it is false, then sends callback about nonexistent command, otherwise do nothing
    ignore_plugin_errors        = false  # if it is false, then ezbotf will show notify about the plugin errors, otherwise do nothing
    ignore_disallow_access      = true   # if it is false, then all disallowed access attempts will be replied to the chat

.. note:: This is an default instance configuration by path ``ezbotf/env_default/instances/default.toml``.
    This configuration generates by default, if you use ``ezbotf -i ...`` command.

.. warning:: By default there is ``api_id = 1`` and ``api_hash = ''`` (unfilled).
    This credentials field MUST be filled! (Get these credentials you can there:
    https://my.telegram.org/ )


``name`` (*str*) field
----------------------

Defines name of the instance.

Example:

.. code-block:: toml

    name = "DefaultInstance"

``prefixes`` (*list[str]*) field
---------------------------------

Defines available prefixes of the instance.

Example:

.. code-block:: toml

    prefixes = ['ez', 'easy', 'изи', 'ізі']

``language`` (*str*) field
--------------------------

Defines language of the instance.

.. note:: You **MUST** use language codes, such as `en` (English), `uk` (Ukrainian),
    `pl` (Polish), `ru` (Russian). This languages for the example

.. note:: By default, **ezbotf** implements only English translation.

Example:

.. code-block:: toml

    language = 'en'

``api_id`` (*int*) field (required to fill)
-------------------------------------------

API ID from https://my.telegram.org/ (go Apps)

Example:

.. code-block:: toml

    api_id = 12345678

``api_hash`` (*int*) field (required to fill)
---------------------------------------------

API HASH from https://my.telegram.org/ (go Apps)

Example:

.. code-block:: toml

    api_hash = 'aaaabbbbccccddddeeeefff123456789'

``[dirs]`` header
-----------------

``dirs`` headers contains paths to the required directories.

There is required directories:

* ``[dirs] plugins_dir``     (*str*)  - Path to directory with the plugins.
* ``[dirs] cache_dir``       (*str*)  - Path to directory with the cache.
* ``[dirs] logs_dir``        (*str*)  - Path to directory with the logs.
* ``[dirs] lang_dir``        (*str*)  - Path to directory with the translations of the instance interface.
* ``[dirs] permissions_dir`` (*str*)  - Path to directory with the permissions store.

.. note:: There no requirement to create new permissions directory with for each instance.
    Permissions folder contains ``<INSTANCE NAME>.toml`` files, where is already defined permissions.

Example:

.. code-block:: toml

    [dirs]
    plugins_dir = './plugins/'
    cache_dir   = './cache/'
    logs_dir    = './logs'
    lang_dir    = './lang/'

``[logging]`` header
--------------------

``logging`` headers contains settings for the logging of the instance.

There is defined these **log levels** (is required for ``console_log_level`` and
``file_log_level`` fields):

* ``DEBUG``      = 1
* ``EXCEPTION``  = 2
* ``INFO``       = 5
* ``WARNING``    = 10
* ``ERROR``      = 15
* ``CRITICAL``   = 20

Example:

.. code-block:: toml

    [logging]
    console_log_level  = 2  # EXCEPTION
    file_log_level     = 1  # DEBUG

    # format of the time for name of the log file
    time_format = '{year:04d}.{month:02d}.{day:02d}_{hour:02d}_{minute:02d}_{second:02d}.{microsecond:04s}'

``[logging] console_log_level`` (*int*) field
---------------------------------------------

Level of logging to the console.

About the **log levels** see above (in ``[logging]`` header).

Example:

.. code-block::

    console_log_level = 5 # INFO

``[logging] file_log_level`` (*int*) field
------------------------------------------

Level of logging to the file.

About the **log levels** see above (in ``[logging]`` header).

Example:

.. code-block::

    file_log_level = 1 # DEBUG

``[logging] time_format`` (*str*) field
---------------------------------------

Format of the time for name of the log file.

Example:

.. code-block::

    time_format = '{year:04d}.{month:02d}.{day:02d}_{hour:02d}_{minute:02d}_{second:02d}.{microsecond:04s}'

``[warnings]`` header
---------------------

``warnings`` headers contains settings of the warnings\errors to show.

``[warnings] ignore_nonexistent_command`` (*bool*) field
--------------------------------------------------------

If it is ``true`` value, when **EzBot Framework** ignores when nonexistent command is typed.
Otherwise, if it is ``false`` value, **EzBot Framework** will send callback about it.

``[warnings] ignore_plugin_errors`` (*bool*) field
--------------------------------------------------

If it is ``true`` value, when **EzBot Framework** ignores plugin exceptions. Otherwise, if it is
``false`` value, **EzBot Framework** will send notifies about plugin exceptions.

``[warnings] ignore_disallow_access`` (*bool*) field
----------------------------------------------------

If it is ``true`` value, when **EzBot Framework** ignores disallowed access to the commands.
Otherwise, if it is ``false`` value, **EzBot Framework** will reply to the user that tried
to run a command.
