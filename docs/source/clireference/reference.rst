.. _cli-main:

=========
Reference
=========

Main
----

Example:

.. code-block::

    ezbotf -h

``-h``, ``--help`` - Shows help message.

``--version`` - Shows current framework version.

``--author`` - Shows author.

``-v``, ``--verbose`` - Show additional information.

``-i (FOLDER NAME)``, ``--initialize (FOLDER NAME)`` - Initializes new environment.

Subcommand: instance
--------------------

Example:

.. code-block::

    ezbotf instance -h

``-h``, ``--help`` - Shows help message about this subcommand.

``-n (NAME)``, ``--new-intance (NAME)`` - Creates new instance in the current environment.

``-r (NAME)``, ``--run (NAME)`` - Runs instance by it name.

``-s (NAME)``, ``--setup (NAME)`` - Set ups credentials for instance by it name. Requires:
**--api-id**, **--api-hash** parameters

``--api-id (API ID)`` - Telegram API ID for **--setup**

``--api-hash (API HASH)`` - Telegram API HASH for **--setup**

.. seealso:: :ref:`firstinstance`

Subcommand: plugin
------------------

``-h``, ``--help`` - Shows help message about this subcommand.

``-i (NAME)``, ``--instance (NAME)`` - Instance with that work. Required for all parameters in ``plugin`` subcommands

``-n (NAME)``, ``--new-plugin (NAME)`` - Creates new plugin.

``-r (NAME)``, ``--remove-plugin (NAME)`` - Removes the plugin.

``-c (NAME)``, ``--compile-plugin (NAME)`` - Compiles the plugin to .zip (do not forget to backup your code!)

``-I (PATH)``, ``--install-plugin (PATH)`` - Installs the plugin.
