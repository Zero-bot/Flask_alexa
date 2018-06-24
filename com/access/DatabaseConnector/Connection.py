from mysql.connector import connection
from mysql.connector import errorcode
from mysql.connector import Error
from com.helpers.ConfigParser import ConfigurationLoader


class Connection:
    config = None

    def __init__(self, config_id):
        loader = ConfigurationLoader()
        self.config = {'user': loader.load(config_id, 'user'),
                       'host': loader.load(config_id, 'host'),
                       'database': loader.load(config_id, 'database'),
                       'password': loader.load(config_id, 'password')}

    def connect(self):
        try:
            return connection.MySQLConnection(**self.config)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
