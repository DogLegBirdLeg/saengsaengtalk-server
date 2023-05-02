from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from logic.delivery.comment.domain.entity.Comment import Comment
from typing import List


class MongoDBCommentRepository(CommentRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_comment_by_id(self, _id) -> Comment:
        find = {'_id': _id}
        comment_json = self.db.comment.find_one(find)
        if comment_json is None:
            raise Exception

        return Comment(_id=comment_json['_id'],
                       post_id=comment_json['post_id'],
                       create_at=comment_json['create_at'],
                       user_id=comment_json['user_id'],
                       nickname=comment_json['nickname'],
                       status=comment_json['status'],
                       content=comment_json['content'],
                       super_comment_id=comment_json['super_comment_id'])

    def find_all_comment_by_post_id(self, post_id) -> List[Comment]:
        find = {'post_id': post_id}
        comments_json = self.db.comment.find(find)

        return [
            Comment(_id=comment_json['_id'],
                    post_id=comment_json['post_id'],
                    create_at=comment_json['create_at'],
                    user_id=comment_json['user_id'],
                    nickname=comment_json['nickname'],
                    status=comment_json['status'],
                    content=comment_json['content'],
                    super_comment_id=comment_json['super_comment_id'])
            for comment_json in comments_json
        ]

    def save(self, comment: Comment):
        data = {
            '_id': comment._id,
            'post_id': comment.post_id,
            'create_at': comment.create_at,
            'user_id': comment.user_id,
            'nickname': comment.nickname,
            'status': comment.status,
            'content': comment.content,
            'super_comment_id': comment.supper_comment_id
        }

        self.db.comment.insert_one(data)

    def delete(self, comment_id):
        find = {'_id': comment_id}
        update = {
            '$set': {
                'status': 'deleted'
            }
        }
        self.db.comment.update_one(find, update)
