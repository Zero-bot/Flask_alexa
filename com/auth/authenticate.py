import com.access.database_operations as db_op


def auth(user_name, key):
    user_data = db_op.fetch_user_data(user_name)
    if user_data.get('key') == key:
        return True
    return False


def get_user_data(user_name):
    return db_op.fetch_user_data(user_name)


def create_user(user_name):
    user_id = db_op.create_user(user_name)
    if user_id.get('status') != 'success':
        raise Exception('User already exist')
    return {'user_id': user_id}


def update_last_login(user_name):
    return db_op.update_last_login(user_name)