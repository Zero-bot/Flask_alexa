class Session:
    admin = None
    session_dict = None

    def __init__(self, session_dict):
        self.session_dict = session_dict
        self.admin = 'ADMIN'

    def destroy_session(self, session_vars):
        for value in session_vars:
            self.session_dict.pop(value, None)

    def is_valid_session(self):
        if self.session_dict:
            if self.session_dict['logged']:
                return True
            return False
        return False

    def is_admin(self):
        return self.session_dict['role'] == self.admin
