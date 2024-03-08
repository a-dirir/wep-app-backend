


class Authenticator:
    def __init__(self, db):
        self.db = db

    def authenticate(self, user: dict):
        return True

