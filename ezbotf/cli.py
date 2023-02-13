"""
CLI helper for manage a framework data
"""

import argparse
import shutil
import pathlib
import tomli_w
import sys

import ezbotf


def get_instance(name: str) -> ezbotf.BotInstance | None:
    """Getting and initializes instance

    :param name: Name of instance to get

    :returns: Instance with imported config or None if it is not initialized
    """

    # check if folder is ezbotf instance
    if not pathlib.Path('./.ezbotf').exists():
        print('ERROR: This is not ezbotf instance folder')
        return

    config_path = pathlib.Path(f'./instances/{name}.toml')

    # check if config exists
    if not config_path.exists():
        print(f'ERROR: There is no instance with name "{name}"')
        return

    # initialize instance
    instance = ezbotf.BotInstance()
    instance.import_config(config_path)

    return instance


def initialize_environment(name: str):
    """Initializes new environment in new folder of current directory

    :param name: Name of the new environment
    """
    # create path to new instance
    new_env_path = pathlib.Path.cwd() / name
    # new_instance_path.mkdir(exist_ok=True)

    # copy default instance to current path
    shutil.copytree(pathlib.Path(__file__).parent / 'templates/environment', new_env_path)


def setup_instance(name: str, api_id: int, api_hash: str):
    """Setups existent instance

    :param name: Name of the instance
    :param api_id: API ID for the instance
    :param api_hash: API HASH for the instance
    """

    # get instance
    instance = get_instance(name)
    if not instance:
        return

    instance.config['api_id']     = api_id
    instance.config['api_hash']   = api_hash

    pathlib.Path(f'./instances/{name}.toml').write_text(tomli_w.dumps(instance.config))


def run_instance(name: str):
    """Runs instance

    :param name: Name of instance
    """

    # get instance
    instance = get_instance(name)
    if not instance:
        return

    # runs instance
    instance.quick_run()


####


def new_instance(name: str):
    """Creates new instance by name

    :param name: Name of the instance
    """

    # check if folder is ezbotf instance
    if not pathlib.Path('./.ezbotf').exists():
        print('ERROR: This is not ezbotf instance folder')
        return

    new_instance_path = pathlib.Path(f'./instances/{name}.toml')

    # copy default instance
    shutil.copyfile(pathlib.Path(__file__).parent / 'env_default/instances/default.toml',
                    new_instance_path)

    new_instance_path.write_text(new_instance_path.read_text().replace('DefaultInstance', name))


####


def new_plugin(name: str, instance_name: str, empty: bool = False):
    """Creates new plugin

    :param name: Name of the new plugin
    :param instance_name: Name of the instance
    :param empty: Create empty template?
    """

    # get instance
    instance = get_instance(instance_name)

    # check if instance successfully gotten
    if not instance:
        print('Cannot to create the plugin')
        return

    # get plugins dir
    plugins_dir = pathlib.Path(instance.config['dirs']['plugins_dir'])

    # check if plugins directory is exists
    if not (plugins_dir.exists() and plugins_dir.is_dir()):
        plugins_dir.mkdir(parents=True)

    # get directory of the plugin
    plugin_dir = plugins_dir / name.lower()

    # check if directory is exists
    if plugin_dir.exists():
        print('Plugin already exists')
        return

    # copy template to new plugin folder
    shutil.copytree(pathlib.Path(__file__).parent / 'templates' / f'plugin_{"empty" if empty else "example"}', plugin_dir)


def remove_plugin(name: str, instance_name: str):
    """Removes plugin

    :param name: Name of the plugin
    :param instance_name: Name of the instance
    """

    # get instance
    instance = get_instance(instance_name)

    # check if instance successfully gotten
    if not instance:
        print('Cannot to create the plugin')
        return

    # get plugins dir
    plugins_dir = pathlib.Path(instance.config['dirs']['plugins_dir'])

    # check if plugins directory is exists
    if not (plugins_dir.exists() and plugins_dir.is_dir()):
        print('Plugins directory for it instance isn\'t exists!')
        return

    # get directory of the plugin
    plugin_dir = plugins_dir / name.lower()

    # check if directory is exists
    if not plugin_dir.exists():
        print('Plugin isn\'t exists')
        return

    try:
        shutil.rmtree(plugin_dir)
    except Exception as e:
        print(f'Cannot to remove plugin. Exception: {e}')


def compile_plugin(name: str, instance_name: str):
    """Compiles the plugin

    :param name: Name of the plugin
    :param instance_name: Name of the instance
    """

    # get instance
    instance = get_instance(instance_name)

    # check if instance successfully gotten
    if not instance:
        print('Cannot to create the plugin')
        return

    # get plugins dir
    plugins_dir = pathlib.Path(instance.config['dirs']['plugins_dir'])

    # check if plugins directory is exists
    if not (plugins_dir.exists() and plugins_dir.is_dir()):
        print('Plugins directory for it instance isn\'t exists!')
        return

    # get directory of the plugin
    plugin_dir = plugins_dir / name.lower()

    # check if directory is exists
    if not plugin_dir.exists():
        print('Plugin isn\'t exists')
        return

    ezbotf.common.compile_plugin(plugin_dir, pathlib.Path.cwd() / f'{name}.plugin')


def install_plugin(path: pathlib.Path, instance_name: str):
    """Installs plugin

    :param path: Path to the compiled plugin
    :param instance_name: Name of the instance
    """

    # check if path format is plugin
    if not path.name.endswith('.plugin.zip'):
        print('Plugins must ends with .plugin.zip')
        return

    # get instance
    instance = get_instance(instance_name)

    # check if instance successfully gotten
    if not instance:
        print('Cannot to create the plugin')
        return

    # get plugins dir
    plugins_dir = pathlib.Path(instance.config['dirs']['plugins_dir'])

    # check if plugins directory is exists
    if not (plugins_dir.exists() and plugins_dir.is_dir()):
        plugins_dir.mkdir(parents=True)

    # get directory of the plugin
    plugin_dir = plugins_dir / path.name.lower()

    # check if directory is exists
    if plugin_dir.exists():
        print('Plugin already exists')
        return

    # try to install a plugin
    ezbotf.common.install_plugin(plugins_dir, path)

####


def check_version():
    """Checks if current running version of python is equals or above 3.11"""

    if not sys.version_info >= (3, 11):
        print('ERROR: EzBotF requires Python 3.11 or above!')
        sys.exit('Mismatch required version of Python')

####


def main():
    """Main function for the CLI"""

    check_version()

    parser = argparse.ArgumentParser(description='help with EzBot Framework management')

    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + ezbotf.version.ezbotf_version_string_full,
                        help='show program version')
    parser.add_argument('--author', action='version',
                        version='ftdot (https://github.com/ftdot)',
                        help='show author of program')

    parser.add_argument('-i', '--initialize',
                        metavar='FOLDER NAME',
                        help='initialize new environment in the given folder name')

    subparsers = parser.add_subparsers(help='Subcommands for ')

    # instance management
    instance_parser = subparsers.add_parser('instance',
                                            help='Manipulate instances')
    instance_parser.add_argument('-n', '--new-instance',
                                 metavar='NAME',
                                 help='create new instance in current ezbotf environment')
    instance_parser.add_argument('-r', '--run',
                                 metavar='NAME',
                                 help='run instance by it name')

    instance_parser.add_argument('-s', '--setup',
                                 metavar='NAME',
                                 help='setup instance by it name. Requires: --api-id, --api-hash')
    instance_parser.add_argument('--api-id',
                                 type=int,
                                 help='telegram API ID parameter for the --setup parameter')
    instance_parser.add_argument('--api-hash',
                                 help='telegram API HASH parameter for the --setup parameter')

    # plugin management
    plugin_parser = subparsers.add_parser('plugin',
                                          help='Plugins management in the current instance')
    plugin_parser.add_argument('-i', '--instance',
                               help='instance with that manipulate. Required for all parameters')
    plugin_parser.add_argument('-n', '--new-plugin',
                               metavar='NAME',
                               help='create new plugin')
    plugin_parser.add_argument('-r', '--remove-plugin',
                               metavar='NAME',
                               help='remove plugin with giblets')
    plugin_parser.add_argument('-c', '--compile-plugin',
                               metavar='NAME',
                               help='compile plugin to .zip (DO NOT FORGET BACKUP YOUR CODE!)')
    plugin_parser.add_argument('-I', '--install-plugin',
                               metavar='PATH',
                               help='install plugin to the instance')
    plugin_parser.add_argument('--empty',
                               action='store_true',
                               default=False,
                               help='(use only with --new-plugin param) create empty plugin')

    args = parser.parse_args()
    args_ = dir(args)

    if 'initialize' in args_ and args.initialize:
        initialize_environment(args.initialize)

    elif 'run' in args_ and args.run:
        run_instance(args.run)

    elif 'setup' in args_ and args.setup:
        if not (args.api_id and args.api_hash):
            instance_parser.print_help()

            print('--api-id, --api-hash parameters is required!')
            exit()

        setup_instance(args.setup, args.api_id, args.api_hash)

    elif 'new_instance' in args_ and args.new_instance:
        new_instance(args.new_instance)

    elif 'new_plugin' in args_ and args.new_plugin:
        if not args.instance:
            plugin_parser.print_help()

            print('-i, --instance parameter is required!')
            exit()

        new_plugin(args.new_plugin, args.instance)

    elif 'remove_plugin' in args_ and args.remove_plugin:
        if not args.instance:
            plugin_parser.print_help()

            print('-i, --instance parameter is required!')
            exit()

        remove_plugin(args.remove_plugin, args.instance)

    elif 'compile_plugin' in args_ and args.compile_plugin:
        if not args.instance:
            plugin_parser.print_help()

            print('-i, --instance parameter is required!')
            exit()

        compile_plugin(args.compile_plugin, args.instance)

    elif 'install_plugin' in args_ and args.install_plugin:
        if not args.instance:
            plugin_parser.print_help()

            print('-i, --instance parameter is required!')
            exit()

        install_plugin(pathlib.Path(args.install_plugin), args.instance, args.empty)

    else:
        parser.print_help()
