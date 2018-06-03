import configparser


def read_config(key, value):
    config = configparser.RawConfigParser()
    config.read("C:\\Users\\mmahalingam\\\Documents\\database.cfg")
    return config.get(key, value)

