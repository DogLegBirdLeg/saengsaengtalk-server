from logic.delivery.comment.domain.entity.Comment import Comment
from logic.delivery.comment.domain.dto.CommentDto import CommentsDto, MainCommentDto
from logic.delivery.comment.domain.RepositoryInterface import CommentRepository
from logic.delivery.comment.infra.CommentDAO import CommentDAO
from bson import ObjectId
from flask import g
from typing import List
from datetime import datetime


class CommentUseCase:
    def __init__(self, comment_repository: CommentRepository, comment_dao: CommentDAO):
        self.comment_repository = comment_repository
        self.comment_dao = comment_dao

    def get_comments(self, post_id) -> List[MainCommentDto]:
        comments = self.comment_repository.find_all_comment_by_post_id(post_id)
        return CommentsDto.mapping(comments)

    def create_comment(self, post_id, content):
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          datetime=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                          user_id=g.id,
                          nickname=g.nickname,
                          status='created',
                          content=content)

        self.comment_repository.save(comment)

    def create_reply(self, post_id, super_comment_id, content):
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          datetime=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                          user_id=g.id,
                          nickname=g.nickname,
                          status='created',
                          content=content,
                          super_comment_id=super_comment_id)

        self.comment_repository.save(comment)

    def delete(self, _id):
        comment = self.comment_repository.find_comment_by_id(_id)
        comment.delete(g.id)
        self.comment_dao.update_status(_id, 'deleted')

    def modify(self, _id, content):
        comment = self.comment_repository.find_comment_by_id(_id)
        comment.modify(g.id, content)
        self.comment_dao.update_content(_id, content)


