from resources.register import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):  # which user with this JWT token has this id in 'users' list ?
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
