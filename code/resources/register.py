from flask_restful import Resource, reqparse

from database.conn import DatabaseConnection
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='password field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()  # parsing the request data
        username, password = data['username'], data['password']
        if UserModel.find_by_username(username):
            return {'message': 'Username already exists'}, 400
        else:
            insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"  # we don't have to specify the id, SQL creates one for us because we used 'id INTEGER PRIMARY KEY'
            try:
                with DatabaseConnection('./database/data.db') as cursor:  # using our context manager (conn.py)
                    cursor.execute(insert_query, (username, password))  # username and password we got from the request (line 48)
            except:
                return {'message': 'error occurred while registering'}, 500
            else:
                return {'message': 'user created successfully'}, 201
