"""
Some utilities (in most for plugins) of framework
"""

import tomlkit
import pathlib
import hashlib
import verlib

import sys
import time
import subprocess

import asyncio
import nest_asyncio

from . import ezlog
from .plugin import Plugin
from .translator import Translator
from .version import ezbotf_version_string
from .permissions import Permissions

from typing import Any, Coroutine
from .types import TOMLDict, PermissionsList, PermissionsDict, VersionSpecific, REQUIRED_PLUGINS_LIST

nest_asyncio.apply()

__all__ = ['check_config', 'check_config_by_path', 'get_translator_for_plugin', 'load_runtime_config',
           'install_requirements_by_path', 'install_requirements', 'check_required_plugins',
           'run_coroutine_without_await', 'compare_versions', 'mask_phone_number', 'sort_by_priority',
           'load_permissions', 'have_permissions']


def check_config(config: TOMLDict, requires: list[str]) -> bool:
    """Checks if given config is valid by ``requires`` list

    :param config: Config dictionary to check
    :param requires: List with the required fields

    :returns: True if config is valid by all required fields, otherwise False
    """

    for e in requires:
        if e not in config:
            return False

    return True


def check_config_by_path(config: TOMLDict, requires: TOMLDict) -> bool:
    """Advanced check for the config is valid. Uses ``requires`` as dictionary.
    Uses :func:`check_config`.

    :param config: Config dictionary to check
    :param requires: Dictionary with required fields

    :returns: True if config is valid by all required fields, otherwise False
    """

    for path, requires_ in requires.items():
        if path.startswith('-'):
            path = path[1:]
        if isinstance(requires_, dict):
            if not check_config_by_path(config[path], requires_):
                return False

            continue

        if not check_config(config[path], requires_):
            return False

    return True


####


def get_translator_for_plugin(plugin: Plugin, desired_lang: str) -> Translator:
    """Loads a translator from the :class:`Plugin` with desired language

    :param plugin: Plugin from get all required configurations to load translator
    :param desired_lang: Desired language to use in translations

    :returns: Initialized :class:`Translator` object
    """

    return Translator(plugin.dir / 'lang', plugin.logger.group,
                      default_lang=plugin.config['lang']['default'],
                      desired_lang=desired_lang)


def load_runtime_config(plugin: Plugin) -> TOMLDict:
    """Loads runtime configuration from the :class:`Plugin`

    :param plugin: Plugin from get all required configurations to get runtime configuration

    :returns: TOML dictionary with the runtime configuration
    """

    # define paths to configs
    default_path = plugin.dir / 'config' / 'default.toml'
    working_path = plugin.dir / 'config' / 'working.toml'

    # check if default config is exists
    if not default_path.exists():
        plugin.logger.error('Cannot to find "default.toml" config!')
        plugin.fail()

    # check if working config is exists
    if working_path.exists():
        # define path to the hash of the default config
        hash_path_default = pathlib.Path(plugin.context.cache_dir) / f'plugin_{plugin.config["name"]}_config_default'

        # check if path to the hash is exists
        if hash_path_default.exists():
            # compare cached hash and now-checked hash
            if hashlib.md5(default_path.read_bytes()).hexdigest() != hash_path_default.read_text():
                plugin.context.notifies.append(f'Config of the plugin "{plugin.config["name"]}" updated')

                # update working config
                config_to_save = tomlkit.loads(default_path.read_text(encoding='utf8'))
                config_to_save.update(tomlkit.loads(working_path.read_text(encoding='utf8')))
                working_path.write_text(tomlkit.dumps(config_to_save), encoding='utf8')

                # write new hash
                hash_path_default.write_text(hashlib.md5(default_path.read_bytes()).hexdigest())

                return config_to_save

        else:
            # creating file with the hash of the default config
            hash_path_default.touch()
            hash_path_default.write_text(hashlib.md5(default_path.read_bytes()).hexdigest())
    else:
        # create working path
        working_path.touch()
        working_path.write_bytes(default_path.read_bytes())

    return dict(tomlkit.loads(working_path.read_text(encoding='utf8')))


####


def install_requirements_by_path(requirements_path: pathlib.Path, pip_logs_dir: pathlib.Path) -> bool | Exception:
    """Tries to install a requirements file by path. With output log of pip

    :param requirements_path: Path to the requirements file
    :param pip_logs_dir: Path to the directory with the pip logs store

    :returns: True if pip successfully installed, otherwise returns an `Exception`
    """

    try:
        l_f = open(pip_logs_dir / f'pip-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}.log',
                   'w')

        # run PIP to install the package
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', requirements_path],
            stdout=l_f
        )

        l_f.close()

        return True
    except Exception as e:
        return e


def install_requirements(plugin: Plugin) -> bool:
    """Installs requirements for the :class:`Plugin`

    :param plugin: Plugin from get required configuration to install requirements

    :returns: True if install is successful, otherwise False
    """

    requirements_path = plugin.dir / plugin.config['requirements']['file']

    if not requirements_path.exists():
        plugin.logger.critical(f'Requested to install requirements, but file "{str(requirements_path)}" doesn\'t exists!'
                               ' Plugin failed')
        plugin.fail()
        return False

    result = install_requirements_by_path(requirements_path,
                                          pathlib.Path(plugin.context.instance.config['dirs']['logs_dir']))

    if isinstance(result, Exception):
        plugin.logger.exception('Exception in {}', 'ezbotf.utils.install_requirements_by_path()', exception=result)
        return False
    else:
        return True


def check_required_plugins_by_list(plugin: Plugin,
                                   plugins: list[Plugin],
                                   required_plugins: REQUIRED_PLUGINS_LIST) -> bool:
    """Check if the required plugins with the required versions are alive.
    Required plugins gets by path ``requirements.plugins`` from plugin config file

    :param plugin: Plugin that uses this function
    :param plugins: Current plugins list
    :param required_plugins: Required plugins list

    :returns: True if all checks are passed, otherwise False
    """

    plugins_dict_by_names = {p.config['name']: p for p in plugins}

    for r in required_plugins:
        checks_count = len([None for e in r if isinstance(e, list)])

        # check count of checks count (allow only 2)
        if checks_count == 0 or checks_count > 2:
            plugin.logger.critical('UTILS: Incorrect count of version checks')
            return False

        # check if required plugin in the dict
        if r[0] not in plugins_dict_by_names:
            plugin.logger.error('{} Missing plugin {}', 'UTILS:', r[0])
            return False

        # get plugin
        p = plugins_dict_by_names[r[0]]

        checks = [compare_versions([p.config['version']] + r[1], plugin.logger)]

        if checks_count == 2:
            checks.append(compare_versions([p.config['version']] + r[2]))

        if not all(checks):
            plugin.logger.error('{} This plugin is incompatible with plugin {}', 'UTILS:', r[0])
            return False

    return True


def check_required_plugins(plugin: Plugin) -> bool:
    """Checks all required plugins for a :class:`Plugin`.
    Shorthand for the :func:`check_required_plugins_by_list`

    :param plugin: Plugin from get all required configurations to check all required plugins

    :returns: True if all checks are passed, otherwise False
    """

    return check_required_plugins_by_list(plugin,
                                          plugin.context.instance.pluginloader.plugins,
                                          plugin.config['requirements']['plugins'])

####


def run_coroutine_without_await(coroutine: Coroutine) -> Any:
    """Runs a coroutine without "await" construction (outside of event loop)

    :param coroutine: Coroutine to run

    :returns: Result of the coroutine
    """

    return asyncio.get_event_loop().run_until_complete(coroutine)


####

allowed_operations = ['>', '<', '>=', '<=', '==', '!=']


def compare_versions(operation: VersionSpecific, logger: ezlog.Logger) -> bool:
    """Compares versions

    :param operation: An operation (versions specific) to compare
    :param logger: Logger to use

    :returns: True if comparing is passed, otherwise False
    """

    logger.debug('{} Compare versions {}', 'UTILS:', operation)

    try:
        first_version = verlib.NormalizedVersion(operation[0])
        second_version = verlib.NormalizedVersion(operation[2])

    except Exception as e:
        logger.error('{} While comparing version {} got an exception', 'UTILS:', operation)
        logger.exception('Exception in {}', 'ezbotf.utils.compare_version()', exception=e)
        return False

    if operation[1] not in allowed_operations:
        return False

    try:
        return eval(f'first_version {operation[1]} second_version')
    except Exception as e:
        logger.error('{} While comparing version {} got an exception', 'UTILS:', operation)
        logger.exception('Exception in {}', 'ezbotf.utils.compare_version()', exception=e)
        return False


def mask_phone_number(number: str) -> str:
    """Mask phone number with *, but show last four numbers. Also, adds a "+" at the start of number string

    :param number: Strings number to mask

    :returns: Masked number string
    """

    return '+'+'*'*(len(number)-4)+number[-4:]


def sort_by_priority(plugins: list[Plugin]) -> list[Plugin]:
    """Sorts given plugin list by priority

    :param plugins: Plugin list to sort

    :returns: List with the sorted plugins
    """

    # list with the plugins sorted by priority
    plugins_dict = {}

    for p in plugins:
        pr = p.config['priority']  # priority of the plugin

        if pr not in plugins_dict:
            plugins_dict[pr] = []

        plugins_dict[pr].append(p)

    for pr in plugins_dict:
        plugins_dict[pr] = sorted(plugins_dict[pr])

    sorted_plugins_dict = {}

    for k in sorted(plugins_dict):
        sorted_plugins_dict[k] = plugins_dict[k]

    sorted_plugins_list = []

    for pl in sorted_plugins_dict.values():
        sorted_pl = sorted(pl, key=lambda p: p.config['name'])
        sorted_plugins_list += sorted_pl

    return sorted_plugins_list


####


def load_permissions(permissions_dir: pathlib.Path, name: str) -> TOMLDict:
    """Loads the permissions from the permissions directory by the instance name

    :param permissions_dir: Path to the directory with the permissions
    :param name: Name of the instance

    :returns: TOML dictionary with the permissions
    """

    permissions_file = permissions_dir / f'{name}.toml'

    if not permissions_file.exists():
        permissions_file.touch()
        return {}

    return dict(tomlkit.loads(permissions_file.read_text(encoding='utf8')))


def save_permissions(permissions_dir: pathlib.Path, name: str, permissions: PermissionsDict):
    """Saves the permissions to the permissions directory by the instance name

    :param permissions_dir: Path to the directory with the permissions
    :param name: Name of the instance
    :param permissions: Permissions dictionary to save
    """

    (permissions_dir / f'{name}.toml').write_text(tomlkit.dumps(permissions), encoding='utf8')


def have_permissions(user_id: str,
                     permissions: PermissionsDict,
                     required_permissions: PermissionsList) -> bool:
    """Checks if the user (by id) have some permissions

    :param user_id: ID of the user
    :param permissions: Dictionary with the all permissions defined
    :param required_permissions: Required permissions

    :returns: True if the user have required permissions (or above), otherwise False
    """

    if user_id not in permissions:
        return Permissions.Any in command_permissions

    if Permissions.Blacklisted in permissions[user_id]:
        return False

    if Permissions.Owner in permissions[user_id]:
        return True

    # check the permissions for user
    for permission in permissions[user_id]:
        if permission in command_permissions:
            return True

        if isinstance(permission, int):
            for cmd_permission in command_permissions:
                if not isinstance(cmd_permission, int):
                    continue

                if permission >= cmd_permission:
                    return True

    return False
