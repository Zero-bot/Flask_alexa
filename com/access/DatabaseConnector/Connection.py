from mysql.connector import connection
from mysql.connector import errorcode
from mysql.connector import Error
from com.helpers.ConfigParser import read_config


def get_config_data(value):
    return read_config('AWS', value)


def read_database_config():
    config_obj = {'user': get_config_data('user'),
                  'host': get_config_data('host'),
                  'database': get_config_data('database'),
                  'password': get_config_data('password')
                  }
    return config_obj


def connect_to_database():
    database_config = read_database_config()
    try:
        return connection.MySQLConnection(**database_config)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
