from typing import List
from logic.delivery.comment.domain.entity.Comment import Comment


class CommentDto:
    def __init__(self, _id, post_id, datetime, user_id, nickname, status, content):
        self._id = _id
        self.post_id = post_id
        self.datetime = datetime
        self.user_id = user_id
        self.nickname = nickname
        self.status = status
        self.content = content


class SubCommentDto(CommentDto):
    @staticmethod
    def mapping(comment: Comment):
        return SubCommentDto(_id=comment._id,
                             post_id=comment.post_id,
                             datetime=comment.datetime,
                             user_id=comment.user_id,
                             nickname=comment.nickname,
                             status=comment.status,
                             content=comment.content)

    @property
    def json(self):
        return {
            '_id': self._id,
            'post_id': self.post_id,
            'datetime': self.datetime,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'status': self.status,
            'content': self.content
        }


class MainCommentDto(CommentDto):
    def __init__(self, _id, post_id, datetime, user_id, nickname, status, content):
        super().__init__(_id, post_id, datetime, user_id, nickname, status, content)
        self.sub_comments: List[SubCommentDto] = []

    @staticmethod
    def mapping(comment: Comment):
        return MainCommentDto(_id=comment._id,
                              post_id=comment.post_id,
                              datetime=comment.datetime,
                              user_id=comment.user_id,
                              nickname=comment.nickname,
                              status=comment.status,
                              content=comment.content)

    @property
    def json(self):
        return {
            '_id': self._id,
            'post_id': self.post_id,
            'datetime': self.datetime,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'status': self.status,
            'content': self.content,
            'sub_comments': [sub_comment.json for sub_comment in self.sub_comments]
        }


class CommentsDto:
    @staticmethod
    def mapping(comments: List[Comment]) -> List[MainCommentDto]:
        main_comments = []
        sub_comment_dict = {}
        for comment in comments:
            if comment.supper_comment_id is None:
                main_comment = MainCommentDto.mapping(comment)
                main_comments.append(main_comment)
                continue

            elif comment.supper_comment_id in sub_comment_dict:
                sub_comment = SubCommentDto.mapping(comment)
                sub_comment_dict[comment.supper_comment_id].append(sub_comment)
                continue

            sub_comment = SubCommentDto.mapping(comment)
            sub_comment_dict[comment.supper_comment_id] = [sub_comment]

        def find_main_comment(_id):
            for main_comment in main_comments:
                if main_comment._id == _id:
                    return main_comment

        for super_comment_id in sub_comment_dict.keys():
            main_comment = find_main_comment(super_comment_id)
            main_comment.sub_comments = sub_comment_dict[main_comment._id]

        return main_comments