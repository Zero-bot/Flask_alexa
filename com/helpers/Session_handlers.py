def invalidate_session(session_dict, session_vars):
    for value in session_vars:
        session_dict.pop(value, None)


def is_valid_session(session_dict):
    if session_dict:
        if session_dict['logged']:
            return True
        return False
    return False


def is_admin(session_dict):
    return session_dict['role'] == 'ADMIN'
