from abc import *


class CommentDAO(metaclass=ABCMeta):
    @abstractmethod
    def update_status(self, _id, status):
        pass

    @abstractmethod
    def update_content(self, _id, content):
        pass


class MongoDBCommentDAO(CommentDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def update_status(self, _id, status):
        find = {'_id': _id}
        data = {
            '$set': {'status': status}
        }
        self.db.comment.update_one(find, data)

    def update_content(self, _id, content):
        find = {'_id': _id}
        data = {
            '$set': {
                'status': 'modified',
                'content': content
            }
        }
        self.db.comment.update_one(find, data)
