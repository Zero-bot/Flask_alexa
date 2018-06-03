import com.access.DatabaseConnector.Connection as awsConnection
import uuid
from mysql.connector import errorcode
from mysql.connector import Error
import configparser


def read_database_config():
    config = configparser.RawConfigParser()
    config.read("C:\\Users\\mmahalingam\\PycharmProjects\\Alexa\com\\access\\DatabaseConnector\\config\\database.cfg")
    config_obj = {'QUERY_USER_DETAILS': config.get('QUERY USERS TABLE', 'user_details'),
                  'QUERY_CREATE_USER': config.get('QUERY USERS TABLE', 'create_user'),
                  'QUERY_UPDATE_LAST_LOGIN': config.get('QUERY USERS TABLE', 'update_last_login')
                  }
    config.clear()
    return config_obj


def fetch_user_data(user_name):
    connection = awsConnection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(read_database_config().get('QUERY_USER_DETAILS'), (user_name,))
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


def create_user(user_name):
    connection = awsConnection.connect_to_database()
    cursor = connection.cursor()
    key = str(uuid.uuid4())
    try:
        cursor.execute(read_database_config().get('QUERY_CREATE_USER'), (user_name, key))
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


def update_last_login(user_name):
    connection = awsConnection.connect_to_database()
    cursor = connection.cursor()
    cursor.execute(read_database_config().get('QUERY_UPDATE_LAST_LOGIN'), (user_name,))
    connection.commit()
    connection.close()