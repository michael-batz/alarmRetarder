import configparser
import threading

class Config:

    def __init__(self, filename):
        self.lock = threading.RLock()
        self.lock.acquire()
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.lock.release()

    def getValue(self, sectionName, key, defaultValue):
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
