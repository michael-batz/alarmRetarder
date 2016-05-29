"""Config module.

This module defines the class for getting and setting configuration
options for alarmRetarder.
"""

import threading
import configparser

class Config(object):
    """Class for handling configuration.

    This class handles the configuration of alarmRetarder. The
    configuration is stored in an ini-file. An instance of this
    class is used for getting and setting values.

    Attributes:
        filename: name of the configuration file.
    """

    def __init__(self, filename):
        """Creates a new config object from the given file"""
        self.__lock = threading.RLock()
        self.__lock.acquire()
        self.__filename = filename
        self.__config = configparser.ConfigParser()
        self.__config.read(filename)
        self.__lock.release()

    def get_value(self, section_name, key, default_value):
        """Gets a configuration value.

        This function returns the configuration value of a specific
        key within a section. If the section/key does not exist,
        the default_value will be returned.

        Args:
            section_name: name of the configuration section.
            key: key of the configuration option.
            default_value: default value.

        Returns:
            The value of the configuration option, or the default
            value, if the configuration option does not exist.
        """
        # set default value
        output = default_value

        # get value from config
        self.__lock.acquire()
        try:
            output = self.__config[section_name][key]
        except:
            pass
        self.__lock.release()

        # return value
        return output

    def set_value(self, section_name, key, value):
        """Sets a configuration value.

        This function sets a configuration value and write the changes
        to the configuration file.

        Args:
            section_name: name of the configuration section.
            key: key of the configuration option.
            value: value of the configuration option.
        """
        self.__lock.acquire()
        # set value in data structure
        try:
            self.__config[section_name]
        except:
            self.__config[section_name] = {}
        self.__config[section_name][key] = value

        # save configuration file
        with open(self.__filename, 'w') as configfile:
            self.__config.write(configfile)
        self.__lock.release()
