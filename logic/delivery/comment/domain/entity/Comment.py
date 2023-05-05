from app import exceptions


class Comment:
    def __init__(self, _id, post_id, create_at, user_id, nickname, status, content, parent_id=None):
        self._id = _id
        self.post_id = post_id
        self.create_at = create_at
        self.user_id = user_id
        self.nickname = nickname
        self.status = status
        self.content = content
        self.parent_id = parent_id if parent_id is None else str(parent_id)

    def _check_permission(self, handling_user_id):
        if handling_user_id != self.user_id:
            raise exceptions.AccessDenied

    def modify(self, handling_user_id, content):
        self._check_permission(handling_user_id)
        self.content = content

    def delete(self, handling_user_id):
        self._check_permission(handling_user_id)
