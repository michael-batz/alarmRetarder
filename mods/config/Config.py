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
        self.lock = threading.RLock()
        self.lock.acquire()
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.lock.release()

    def getValue(self, sectionName, key, defaultValue):
        """Gets a configuration value.

        This function returns the configuration value of a specific
        key within a section. If the section/key does not exist,
        the defaultValue will be returned.

        Args:
            sectionName: name of the configuration section.
            key: key of the configuration option.
            defaultValue: default value.

        Returns:
            The value of the configuration option, or the default
            value, if the configuration option does not exist.
        """
        # set default value
        output = defaultValue

        # get value from config
        self.lock.acquire()
        try:
            output = self.config[sectionName][key]
        except:
            pass
        self.lock.release()

        # return value
        return output

    def setValue(self, sectionName, key, value):
        """Sets a configuration value.

        This function sets a configuration value and write the changes
        to the configuration file.

        Args:
            sectionName: name of the configuration section.
            key: key of the configuration option.
            value: value of the configuration option.
        """
        self.lock.acquire()
        # set value in data structure
        try:
            self.config[sectionName]
        except:
            self.config[sectionName] = {}
        self.config[sectionName][key] = value

        # save configuration file
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
        self.lock.release()
