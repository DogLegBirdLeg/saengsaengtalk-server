from logic.common.push_message.application.port.outgoing.TokenQueryDao import TokenQueryDao


class MongoDBTokenQueryDao(TokenQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_all_registration_token_user_id(self, users):
        find = {'user._id': {'$in': users}}
        projection = {'_id': False, 'registration_token': True}

        tokens = [token['registration_token'] for token in self.db.token.find(find, projection)]
        return tokens
