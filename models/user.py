from database.conn import DatabaseConnection


class UserModel:
    def __init__(self, _id, username, password):  # we use this method to access the user information in the server easily, just by typing User.username for example
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with DatabaseConnection('./database/data.db') as cursor:
            username_query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(username_query, (username,))
            row = result.fetchone()
            if row:
                user = cls(*row)  # unpacks id, username and password of the row that matched the given username
            else:
                user = None

        return user

    @classmethod
    def find_by_id(cls, _id):
        with DatabaseConnection('./database/data.db') as cursor:
            username_query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(username_query, (_id,))
            row = result.fetchone()
            if row:
                user = cls(*row)  # unpacks id, username and password of the row that matched the given id
            else:
                user = None

        return user
