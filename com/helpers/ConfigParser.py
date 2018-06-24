import configparser
import os


class ConfigurationLoader:
    parser = None
    config = None

    def __init__(self):
        if os.name == 'nt':
            self.parser = configparser.RawConfigParser()
            self.parser.read("C:\\Users\\mmahalingam\\Documents\\database.cfg")
        else:
            self.parser = configparser.RawConfigParser()
            self.parser.read(os.environ['FLASK_CONFIG'])

    def load(self, key, value):
        return self.parser.get(key, value)
