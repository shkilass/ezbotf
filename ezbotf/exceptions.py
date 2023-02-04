"""
All exceptions from the framework
"""


class PluginError(Exception):
    """Class for all the plugins errors.
    If you want to create own error, it must inherit

    :ivar plugin_name: Name of the plugin raised exception
    :ivar description: Description of the exception
    """

    def __init__(self, plugin_name: str, description: str, *args):
        """
        :param plugin_name: Name of the plugin that raises the exception
        :param description: Description of the error
        """
        super().__init__(*args)

        self.plugin_name  = plugin_name
        self.description  = description

    def __str__(self):
        return f'Plugin "{self.plugin_name}" ' + self.description


# class ArgumentTypeCastingError(Exception):
#     """Error for the ArgumentParser's type-casts
#
#     :ivar description: Description of the error
#     """
#
#     def __init__(self, description: str, *args):
#         """
#         :param description: Description of the error
#         """
#         super().__init__(*args)
#
#         self.description = description
#
#     def __str__(self):
#         return self.description


class IncorrectInstanceConfigError(Exception):
    """Errors if the config of instance is incorrect

    :ivar config_path: path to the config
    """

    def __init__(self, config_path: str, *args):
        """
        :param config_path: path to the config
        """
        super().__init__(*args)

        self.config_path = config_path

    def __str__(self):
        return f'Incorrect instance config by path "{self.config_path}"'
