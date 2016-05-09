import configparser

class Config:

    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def getValue(self, sectionName, key, defaultValue):
        output = defaultValue
        try:
            output = self.config[sectionName][key]
        except:
            pass

        return output

    def setValue(self, sectionName, key, value):
        # set value in data structure
        try:
            self.config[sectionName]
        except:
            self.config[sectionName] = {}
        self.config[sectionName][key] = value
        
        # save configuration file
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
