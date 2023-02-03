"""
Common utilities for CLI
"""

import os
import pathlib
import py_compile
import shutil


def compile_directory(path: pathlib.Path):
    """Compiles all .py files in the directory (also deletes it and __pycache__)

    :param path: Path to the directory to compile
    """

    for p in path.iterdir():
        if p.name in ['__pycache__']:
            try:
                shutil.rmtree(p)
            except Exception as e:
                print(f'Cannot to delete "__pycache__". Exception: {e}')

        elif p.is_file():
            if p.name.endswith('.py'):
                py_compile.compile(str(p), str(p) + 'c', optimize=2)
                try:
                    os.remove(p)
                except Exception as e:
                    print(f'Cannot to delete "{str(p)}". Exception: {e}')

        elif p.is_dir():
            compile_directory(p)


def compile_plugin(path: pathlib.Path, out_path: str):
    """Compiles plugin for transport it

    :param path: Path to the plugin directory
    :param out_path: Path to the directory where be exported compiled plugin and raw plugin directory
    """
    compile_directory(path)
    shutil.copytree(path, out_path + '-raw')
    shutil.make_archive(out_path, 'zip', path)


def install_plugin(plugins_dir: pathlib.Path, plugin_zipped_path: pathlib.Path) -> bool:
    """Installs plugin by path

    :param plugins_dir: Directory with the plugins
    :param plugin_zipped_path: Path to compiled & zipped plugin

    :returns: True if plugin successfully installed, otherwise False
    """

    plugin_dir = plugins_dir / plugin_zipped_path.name[:-11]

    try:
        plugin_dir.mkdir()
    except Exception as e:
        print(f'Can\'t create plugin directory. Exception: {e}')
        return False

    shutil.unpack_archive(str(plugin_zipped_path), plugin_dir)

    return True
