from app import exceptions
from bson import ObjectId

from blinker import signal

post_event = signal('post-event')


class Post:
    def __init__(self, _id, store_id, user_id, nickname, status, place, order_time, min_member, max_member, fee, users):
        self._id = _id
        self.store_id = store_id
        self.user_id = user_id
        self.nickname = nickname
        self.status = status
        self.place = place
        self.order_time = order_time
        self.min_member = min_member
        self.max_member = max_member
        self.fee = fee
        self.users = users

    @staticmethod
    def create(store_id, user_id, nickname, place, order_time, min_member, max_member, order_json):
        post = Post(_id=str(ObjectId()),
                    store_id=store_id,
                    user_id=user_id,
                    nickname=nickname,
                    status='recruiting',
                    place=place,
                    order_time=order_time,
                    min_member=min_member,
                    max_member=max_member,
                    fee=0,
                    users=[user_id])

        post_event.send('created', post_id=post._id, store_id=store_id, user_id=user_id, nickname=nickname, order_json=order_json)
        return post

    def _check_permission(self, user_id):
        if self.user_id != user_id:
            raise exceptions.AccessDenied

    def _check_modifiable(self):
        if self.status not in ['recruiting', 'closed']:
            raise exceptions.CantModify

    def modify_content(self, user_id, order_time, place, min_member, max_member):
        self._check_permission(user_id)
        self._check_modifiable()

        self.order_time = order_time
        self.place = place
        self.min_member = min_member
        self.max_member = max_member

    def set_status(self, user_id, status):
        self._check_permission(user_id)
        self._validate_change_status(status)

        self.status = status

        if status == 'ordered':
            post_event.send('ordered', users=self.users, post_id=self._id)

        elif status == 'delivered':
            post_event.send('delivered', users=self.users, place=self.place, post_id=self._id)

    def update_fee(self, user_id, fee):
        self._check_permission(user_id)
        self.fee = fee

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

        elif self.status == 'delivered':
            raise exceptions.NotValidStatus

    def join(self, user_id, nickname, order_json):
        if self.status != 'recruiting':
            raise exceptions.NotRecruiting

        if len(self.users) >= self.max_member:
            raise exceptions.MaxMember

        if user_id in self.users:
            raise exceptions.AlreadyJoinedUser

        self.users.append(user_id)
        post_event.send('joined',
                        owner_user_id=self.user_id,
                        current_member=len(self.users),
                        store_id=self.store_id,
                        post_id=self._id,
                        user_id=user_id,
                        nickname=nickname,
                        order_json=order_json)

    def quit(self, user_id):
        if self.status != 'recruiting':
            raise exceptions.NotRecruiting

        if user_id == self.user_id:
            raise exceptions.OwnerQuit

        if user_id not in self.users:
            raise exceptions.NotJoinedUser

        self.users.remove(user_id)
        post_event.send('quited', post_id=self._id, user_id=user_id)

    def can_delete(self, user_id):
        self._check_permission(user_id)
        self._check_modifiable()
