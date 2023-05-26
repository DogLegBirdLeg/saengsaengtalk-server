from logic.delivery.post.application.port.outgoing.persistence.UserQueryDao import UserQueryDao


class MongoDBUserQueryDao(UserQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_user_account_number(self, user_id):
        find = {'_id': user_id}
        user = self.db.user.find_one(find)
        return user['name'], user['account_number']
