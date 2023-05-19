import exceptions
from datetime import datetime
from bson import ObjectId

from blinker import signal

comment_event = signal('comment-event')


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

    @staticmethod
    def create(post_id, user_id, nickname, content, parent_id=None):
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          create_at=datetime.now(),
                          user_id=user_id,
                          nickname=nickname,
                          status='created',
                          content=content,
                          parent_id=parent_id)

        comment_event.send('created', user_id=user_id, nickname=nickname, content=content, post_id=post_id, parent_id=parent_id)

        return comment

    def _check_permission(self, handling_user_id):
        if handling_user_id != self.user_id:
            raise exceptions.AccessDenied

    def modify(self, handling_user_id, content):
        self._check_permission(handling_user_id)
        self.content = content

    def delete(self, handling_user_id):
        self._check_permission(handling_user_id)
