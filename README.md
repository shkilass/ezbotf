
# EzBot Framework (**In the development**)

This is a beautiful userbot framework for messangers that uses plugin system and have cool features, such as:
- Configurations (Your plugin may have config, such as "browser-to-use". Users of your plugin can change it)
- Translations (You can easily translate framework\plugins to any language by using TOML documents)
- Commands (You can create any command that can be called with prefixes)
- Argument Parser (You can easily add typed arguments to your command)

Currently, framework in the development. This is may cause some bugs or incorrect work of some functions, grammatical errors, undocumented things and other.
If you found any of this, describe it [there](/issues).

See more [on the documentation page](#)


## Contents

- [User Installation](#user-installation)
- - [By PIP](#by-pip)
- - [Manual Installation](#manual-installation)

- [Dev Installation](#dev-installation)

- [Quick Guide To Environment\Instances](#quick-guide-to-environmentinstances)
- - [Creating An Environment](#creating-an-environment)
- - [Creating Own Bot Instance](#creating-own-bot-instance)
- - [Setting Up Bot Instance](#setting-up-bot-instance)
- - [Run Your Bot Instance](#run-your-bot-instance)

- [Quick Guide To Plugins](#quick-guide-to-plugins)
- - [Installing a Plugin](#installing-a-plugin)
- - [Removing a Plugin](#removing-a-plugin)

- [Documentation](#documentation)
- - [Build Documentation](#build-documentation)

<!--
- [EzzBot - Better Place For Users](#ezzbot---better-place-for-users)
-->


## User Installation

**NOTE:** `EzBot Framework` only supports Python 3.10+ versions, I recommend to use Python 3.11.*

User Installation is just for simple users. This installation does not anticipate changes in the framework code.
If you want to contribute the code, see [Dev Installation](#dev-installation)

There are two ways to install this:
- By the Python PIP
- Manual


#### By PIP

Just enter command (WINDOWS):
```shell
pip install ezbotf
```

If your OS is Linux, enter this command:
```shell
pip3 install ezbotf
```


#### Manual Installation

Clone this repository:
```shell
git clone https://github.com/ftdot/ezbotf.git
```

**NOTE:** If you want to clone and use other (dev,unstable) branch, use this command instead of:
```shell
git clone --single-branch -b 1.0.0-dev https://github.com/ftdot/ezbotf.git
```

Enter the repo directory:
```shell
cd ezbotf
```

Run this command (WINDOWS):
```shell
pip install .
```

Or this for Linux:
```shell
pip3 install .
```

## Dev Installation

If you want to edit, contribute, debug, etc. the framework, you need to install `Editable` package.
This allows to edit code and use it in applications (as import) without uninstall\install scheme.
This feature is provided by **PyPI package manager**

Just go to [Manual User Installation](#manual-installation), but instead of last command, use it:

For Windows:
```shell
pip install --editable .
```

For Linux:
```shell
pip3 install --editable .
```


## Quick Guide To Environment\Instances

You can get help for the ezbotf by this command:
```shell
ezbotf -h
```

Also, you can get help with bot instances by this command:
```shell
ezbotf instance -h
```


#### Creating an Environment

You can use a EzBotF-CLI (installs with the EzBotF) to initialize new EzBotF environment:
```shell
ezbotf -i (NAME)
```
> **NOTE:** Replace `(NAME)` with name of environment you need. Name of environment = name of folder

Change current working directory to directory with the environment:
```shell
cd (NAME)
```


#### Creating Own Bot Instance

Create your instance (you can name it with name of account that you will be use):
```shell
ezbotf instance -n (NAME OF INSTANCE)
```
> **NOTE:** You can skip this step and use `default` instance name. This is comes with default environment settings


#### Setting Up Bot Instance

To set up your bot instance, you must have the `API ID` and `API HASH` credentials. You can get it from [my.telegram.org](https://my.telegram.org).
Go to "APPS". And if you don't have app - create and name it. After, you will get `API ID` and `API HASH`

> **NOTE:** Do not share your credentials! If your `API ID\API HASH` will be used for spamming, auto-subscribing, etc. **your account will be banned by Telegram!**

After you get `API ID` and `API HASH`, enter to your environment and enter this command:
```shell
ezbotf instance -s (NAME OF INSTANCE) --api-id (API ID) --api-hash
```

After you do this command, your instance will be successfully setup, and you can run it!


#### Run Your Bot Instance

After you set up environment, set up your bot instance - you can run it by this command:
```shell
ezbotf instance -r (NAME OF INSTANCE)
```
> **NOTE:** By first run, bot instance will ask your telegram credentials. Don't scare, to these credentials nobody have access, only you


## Quick Guide To Plugins

You can get help for the plugins by this command:
```shell
ezbotf plugin -h
```


#### Installing a Plugin

To install plugin, firstly, you need to download it to environment directory.
After you install it, you can type this command:
```shell
ezbotf plugin -i (INSTANCE NAME) -I (PATH TO PLUGIN)
```
> **NOTE:** Path to plugin must ends with ".plugin.zip"


#### Removing a Plugin

To remove a plugin, you can simply type:
```shell
ezbotf plugin -i (INSTANCE NAME) -r (NAME OF PLUGIN)
```
> **NOTE:** Plugin name = plugin directory name, or name without ".plugin.zip" suffix


## Documentation

(There must be link to the documentation)


#### Build Documentation

For first, you need to clone this repository and go to this directory.
If you are not cloned this repo, [see this](#manual-installation)

Enter the `docs` repository:
```shell
cd docs
```

Install requirements:
```shell
pip install -r requirements.txt
```

**WARNING:** Is required to install and use **Make** utility.
Or, on Windows you can use **make.bat** and skip this warning

Build **HTML** docs via **Make**:
```shell
make html
```

<!--
## **EzzBot** - Better Place For Users

**EzzBot** - Is an application-overlay of the EzBot Framework for all platforms (including **Android**) with the GUI and some cool features.
I recommend to use it if you are is user.

At the current moment, this project in the closed development. To get news about it, you can watch [this repo](https://github.com/ftdot/ezbot)
-->
