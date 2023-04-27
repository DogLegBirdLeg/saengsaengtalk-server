from app import exceptions
from bson import ObjectId
from datetime import datetime
from blinker import signal

from logic.delivery.post.domain.vo.store_vo import StoreVO

post_event = signal('post-event')


class Post:
    def __init__(self, _id, title, store: StoreVO, user_id, nickname, status, place, order_time, min_member, max_member, users):
        self._id = _id
        self.title = title
        self.store = store
        self.user_id = user_id
        self.nickname = nickname
        self.status = status
        self.place = place
        self.order_time = order_time
        self.min_member = min_member
        self.max_member = max_member
        self.users = users

    @staticmethod
    def create(user_id, nickname, store: StoreVO, place, order_time, min_member, max_member, order_json):
        title = Post.make_title(order_time, store.name)
        post = Post(_id=str(ObjectId()),
                    title=title,
                    store=store,
                    user_id=user_id,
                    nickname=nickname,
                    status='recruiting',
                    place=place,
                    order_time=order_time,
                    min_member=min_member,
                    max_member=max_member,
                    users=[user_id])

        post_event.send('created', store_id=store._id, post_id=post._id, user_id=user_id, nickname=nickname, order_json=order_json)
        return post

    def _check_permission(self, handling_user_id):
        if self.user_id != handling_user_id:
            raise exceptions.AccessDenied

    def _check_modifiable(self):
        if self.status not in ['recruiting', 'closed']:
            raise exceptions.CantModify

    def modify_content(self, handling_user_id, order_time, place, min_member, max_member):
        self._check_permission(handling_user_id)
        self._check_modifiable()

        title = self.make_title(order_time, self.store.name)
        self.order_time = order_time
        self.title = title
        self.place = place
        self.min_member = min_member
        self.max_member = max_member

    def set_status(self, handling_user_id, status):
        self._check_permission(handling_user_id)
        self._validate_change_status(status)

        self.status = status

    def _validate_change_status(self, status):
        if status not in ['recruiting', 'closed', 'ordered', 'delivered']:
            raise exceptions.NotValidStatus

        if self.status == 'recruiting':
            if status != 'closed':
                raise exceptions.NotValidStatus

        elif self.status == 'closed':
            if status not in ['recruiting', 'ordered']:
                raise exceptions.NotValidStatus

        elif self.status == 'ordered':
            if status != 'delivered':
                raise exceptions.NotValidStatus

    def join(self, handling_user_id, handling_nickname, order_json):
        if self.status != 'recruiting':
            raise exceptions.NotRecruiting

        if len(self.users) >= self.max_member:
            raise exceptions.MaxMember

        if handling_user_id in self.users:
            raise exceptions.AlreadyJoinedUser

        post_event.send('joined', store_id=self.store._id, post_id=self._id, user_id=handling_user_id, nickname=handling_nickname, order_json=order_json)
        self.users.append(handling_user_id)

    def quit(self, handling_user_id):
        if self.status != 'recruiting':
            raise exceptions.NotRecruiting

        if handling_user_id == self.user_id:
            raise exceptions.OwnerQuit

        if handling_user_id not in self.users:
            raise exceptions.NotJoinedUser

        post_event.send('quited', post_id=self._id, user_id=handling_user_id)
        self.users.remove(handling_user_id)

    def can_delete(self, handling_user_id):
        self._check_permission(handling_user_id)
        self._check_modifiable()

    @staticmethod
    def make_title(order_time, store_name):
        return f'[{datetime.fromisoformat(order_time).strftime("%H:%M")}] {store_name}'
