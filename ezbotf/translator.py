"""
Here is defined only :class:`Translator` class that helps with the translations management.
"""

import os.path
import tomllib
import pathlib

from . import ezlog, reprutil

from .types import TOMLDict

__all__ = ['Translator']


class Translator:
    """Translator object provides the easy methods to translate text

    :ivar lang_dir: Path to the directory with the translation files
    :ivar logger_group: Group for the translator logger
    :ivar default_lang: Default language (Lang code)
    :ivar desired_lang: Desired language to use (Lang code)
    :ivar translations: TOML dictionary with the loaded translations
    :ivar logger: Logger of the translator
    """

    def __init__(self,
                 lang_dir: pathlib.Path,
                 logger_group: ezlog.LoggerGroup | str,
                 default_lang: str = 'en',
                 desired_lang: str = 'en'):
        """
        :param lang_dir: Path to the directory with the translation files
        :param logger_group: Group for the translator logger
        :param default_lang: Default language (Lang code)
        :param desired_lang: Desired language to use (Lang code)
        """

        self.lang_dir      = lang_dir
        self.default_lang  = default_lang
        self.desired_lang  = desired_lang

        self.translations: TOMLDict        = {}
        self.logger: ezlog.Logger          = ezlog.Logger('Translator', group=logger_group)

        self._cache: dict[str, str] = {}

        self.initialize()

    def load_file(self, path: pathlib.Path) -> bool:
        """Loads a file to the translations dictionary.
        Note, that if language is not exists, DEBUG log will be recorded about it

        :param path: Path to the file

        :returns: True if language is successfully loaded, otherwise False
        """

        self.logger.debug('Loading language from the file by path {}', str(path))

        if not path.exists():
            self.logger.debug('Path doesn\'t exists. Can\'t load the translations')
            return False

        self.translations = tomllib.loads(path.read_text(encoding='utf8'))

        return True

    def load_language(self, language: str) -> bool:
        """Loads specific language to translations dictionary

        :param language: Language to load

        :returns: True if language is loaded, otherwise False
        """

        return self.load_file(self.lang_dir / f'{language}.toml')

    def initialize(self):
        """Initializes the default translation file (loads it as default_lang)"""

        self.logger.debug('Initializing default {} variant in {} directory', self.default_lang, str(self.lang_dir))

        if not self.load_language(self.desired_lang):
            self.load_language(self.default_lang)

    ####
    
    def _get(self, path: str):
        """Gets translation by string path (keys separated by dots).
        This is private method (that doesn't use caching) you must use :func:`get()`

        """
        path_sep = path.split('.')  # split path by dots

        value = self.translations  # last value of "for" statement

        for p in path_sep:

            if isinstance(value, dict) and p in value:
                value = value[p]
            else:
                value = None
                break

        return value \
            if value is not None else self.translations.get('translation_not_found',
                                                                 'Translation not found. Contact with developer')

    def get(self, path: str, force: bool = False):
        """Gets translation by string path (keys separated by dots).
        Also, formats translation with codes ([newline] as example)
        Example: command.example.names

        :param path: Path to the translation separated by dots

        :returns: Translation, if it exits. Otherwise, "translation_not_found" key
        """

        if path in self._cache and not force:
            return self._cache[path]

        result = self._get(path)
        self._cache[path] = result

        return result

    ####

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return reprutil.get_repr(self)
