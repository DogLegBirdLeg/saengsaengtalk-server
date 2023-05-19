import pymongo
from bson import ObjectId
from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from logic.delivery.comment.domain.entity.Comment import Comment
from typing import List
import exceptions


class MongoDBCommentRepository(CommentRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_comment_by_id(self, comment_id) -> Comment:
        find = {'_id': ObjectId(comment_id)}
        comment_json = self.db.comment.find_one(find)
        if comment_json is None:
            raise exceptions.NotExistComment

        return Comment(_id=str(comment_json['_id']),
                       post_id=str(comment_json['post_id']),
                       create_at=comment_json['create_at'],
                       user_id=comment_json['user_id'],
                       nickname=comment_json['nickname'],
                       status=comment_json['status'],
                       content=comment_json['content'],
                       parent_id=str(comment_json['parent_id']))

    def find_all_comment_by_post_id(self, post_id) -> List[Comment]:
        find = {'post_id': ObjectId(post_id)}
        comments_json = self.db.comment.find(find).sort('create_at', pymongo.ASCENDING)
        return [
            Comment(_id=str(comment_json['_id']),
                    post_id=str(comment_json['post_id']),
                    create_at=comment_json['create_at'],
                    user_id=comment_json['user_id'],
                    nickname=comment_json['nickname'],
                    status=comment_json['status'],
                    content=comment_json['content'],
                    parent_id=comment_json['parent_id'])
            for comment_json in comments_json
        ]

    def save(self, comment: Comment):
        data = {
            '_id': ObjectId(comment._id),
            'post_id': ObjectId(comment.post_id),
            'create_at': comment.create_at,
            'user_id': comment.user_id,
            'nickname': comment.nickname,
            'status': comment.status,
            'content': comment.content,
            'parent_id': comment.parent_id if comment.parent_id is None else ObjectId(comment.parent_id)
        }

        self.db.comment.insert_one(data)

    def delete(self, comment_id):
        find = {'_id': ObjectId(comment_id)}
        update = {
            '$set': {
                'status': 'deleted'
            }
        }
        self.db.comment.update_one(find, update)
