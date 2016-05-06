import configparser

class Config:

    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def getValue(self, sectionName, key, defaultValue):
        output = defaultValue
        try:
            output = self.config[sectionName][key]
        except:
            pass

        return output
