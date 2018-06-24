from com.access.DatabaseConnector.Connection import Connection
from com.helpers.ConfigParser import read_config
from enum import Enum


class Status(Enum):
    ON = 'ON'
    OFF = 'OFF'


class RaspberryDevices:
    database_config = 'QUERY PI STATUS'
    connection = None
    query_get_device = ''
    query_update_device_state = ''

    def __init__(self):
        self.query_get_device = read_config(self.database_config, 'get_device_data')
        self.query_update_device_state = read_config(self.database_config, 'update_device_state')
        self.connection = Connection('AWS').connect()

    def get_device(self, name):
        cursor = self.connection.cursor()
        cursor.execute(self.query_get_device, (name, ))
        device_data = {}
        for device, status, last_accessed, modified_by in cursor:
            device_data = {'device': device,
                           'status': status,
                           'last_accessed': last_accessed,
                           'modified_by': modified_by
                           }
        cursor.close()
        return device_data

    def update_device_state(self, name, status, user):
        cursor = self.connection.cursor()
        cursor.execute(self.query_update_device_state, (status.value, user, name))
        self.connection.commit()
        cursor.close()

    def toggle_device_state(self, name, user):
        current_state = self.get_device(name)['status']
        if current_state == Status.ON.value:
            self.update_device_state(name, Status.OFF, user)
        if current_state == Status.OFF.value:
            self.update_device_state(name, Status.ON, user)

    def terminate_connection(self):
        self.connection.close()
