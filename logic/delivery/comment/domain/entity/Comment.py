from app import exceptions


class Comment:
    def __init__(self, _id, post_id, datetime, user_id, nickname, status, content, super_comment_id=None):
        self._id = _id
        self.post_id = post_id
        self.datetime = datetime
        self.user_id = user_id
        self.nickname = nickname
        self.status = status
        self.content = content
        self.supper_comment_id = super_comment_id

    def _check_permission(self, handling_user_id):
        if handling_user_id != self.user_id:
            raise exceptions.AccessDenied

    def modify(self, handling_user_id, content):
        self._check_permission(handling_user_id)
        self.content = content

    def delete(self, handling_user_id):
        self._check_permission(handling_user_id)
