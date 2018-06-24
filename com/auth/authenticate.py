from com.access.database_operations import DatabaseOperationsWrapper


class DatabaseOperations:
    _database = None

    def __init__(self):
        self._database = DatabaseOperationsWrapper()

    def validate_user(self, user_name, key):
        user_data = self._database.fetch_user_data(user_name)
        if user_data.get('key') == key:
            return True
        return False

    def get_user_data(self, user_name):
        return self._database.fetch_user_data(user_name)

    def create_user(self, user_name):
        user_id = self._database.create_user(user_name)
        if user_id.get('status') != 'success':
            raise Exception('User already exist')
        return {'user_id': user_id}

    def update_last_login(self, user_name):
        return self._database.update_last_login(user_name)
