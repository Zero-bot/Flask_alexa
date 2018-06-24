from com.access.DatabaseConnector.Connection import Connection
import uuid
from mysql.connector import errorcode
from mysql.connector import Error
from com.helpers.ConfigParser import ConfigurationLoader


class DatabaseOperationsWrapper:
    QUERY_USER_DETAILS = None
    QUERY_CREATE_USER = None
    QUERY_UPDATE_LAST_LOGIN = None
    CONFIG = 'QUERY USERS TABLE'
    CONNECTION = Connection('AWS')

    def __init__(self):
        loader = ConfigurationLoader()
        self.QUERY_USER_DETAILS = loader.load(self.CONFIG, 'user_details')
        self.QUERY_CREATE_USER = loader.load(self.CONFIG, 'create_user')
        self.QUERY_UPDATE_LAST_LOGIN = loader.load(self.CONFIG, 'update_last_login')
        self.CONNECTION = Connection('AWS')

    def fetch_user_data(self, user_name):
        connection = self.CONNECTION.connect()
        cursor = connection.cursor()
        cursor.execute(self.QUERY_USER_DETAILS, (user_name,))
        user_data = {}
        for (ID, user, key, created_on, last_login, role, status) in cursor:
            user_data = {'id': ID,
                         'user_name': user,
                         'key': key,
                         'created_on': created_on,
                         'last_login': last_login,
                         'role': role,
                         'status': status
                         }
        connection.close()
        return user_data

    def create_user(self, user_name):
        connection = self.CONNECTION.connect()
        cursor = connection.cursor()
        key = str(uuid.uuid4())
        try:
            cursor.execute(self.QUERY_CREATE_USER, (user_name, key))
            user_id = cursor.lastrowid
            connection.commit()
        except Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                connection.close()
                return {'status': 'duplicate user'}
            else:
                print(err)
                return {'status': 'failure'}
        connection.close()
        return {'id': user_id, 'status': 'success'}

    def update_last_login(self, user_name):
        connection = self.CONNECTION.connect()
        cursor = connection.cursor()
        cursor.execute(self.QUERY_UPDATE_LAST_LOGIN, (user_name,))
        connection.commit()
        connection.close()
