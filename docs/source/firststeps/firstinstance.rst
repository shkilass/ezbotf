.. _firstinstance:

==============
First instance
==============

EzBot Framework is works on instances. Instance - is a set of some configurations,
such as: credentials, name, and other. It created to easily add many messanger accounts
to one environment. Environment - is a folder that contains all for framework work. All
is: plugins, instances, logs, settings, translations and other.

As you know, you need to create environment. With the installation, you have been
installed **EzBotF CLI**. This is an utility to manage environments\instances\plugins.
You can access it via terminal\commandline on all platforms (after installation).

Create environment
------------------

To create environment, open folder in terminal, there you want to store it. After,
enter this command:

.. code-block:: shell

    ezbotf -i <environment name>

.. note:: Replace **<environment name>** with name you want. As example, just **ezbotf**.

Create instance
---------------

To create instance, stay in environment folder and type command:

.. code-block:: shell

    ezbotf instance -n <instance name>

.. note:: Replace **<instance name>** with your instance name. As example, you can name it
    with your account name. You can use **default** instance. It is already exists, you not
    required to create it. But, set up instances to work with them!

Set up your instance
--------------------

You can easily set up your instance. Framework requires Telegram application. To get it,
you can go to https://my.telegram.org/. After, go to Apps and create an application. Name
it how you want.

After, copy **API ID** and **API HASH** and paste to this command:

.. code-block:: shell

    ezbotf instance -s <instance name> --api-id <API ID> --api-hash <API HASH>

After that all, run your instance!

.. code-block:: shell

    ezbotf instance -r <instance name>

For first start, **telethon** will ask you for your credentials. Don't scare, to these
credentials no one have access, only you.

To get more about **CLI** check **CLI Reference**.
