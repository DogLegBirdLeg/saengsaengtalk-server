from app.api.Store.Domain.Model.Store import Store
from datetime import datetime
from app import exceptions
from flask import g
from bson import ObjectId
from typing import List
from blinker import signal
'''
recruiting : 모집중
closed : 마감됨
ordered: 주문 완료
delivered: 배달 완료
'''

post_event = signal('post-event')


class Post:
    def __init__(self,
                 _id: str,
                 title: str,
                 store: Store,
                 user_id: int,
                 nickname: str,
                 status: str,
                 place: str,
                 order_time: str,
                 min_member: int,
                 max_member: int,
                 users: List[int]):
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
    def create(store: Store, place, order_time, min_member, max_member, order_json):
        title = Post.make_title(order_time, store.name)
        post = Post(_id=str(ObjectId()),
                    title=title,
                    store=store,
                    user_id=g.id,
                    nickname=g.nickname,
                    status='recruiting',
                    place=place,
                    order_time=order_time,
                    min_member=min_member,
                    max_member=max_member,
                    users=[g.id])
        post_event.send('created', store_id=store._id, post_id=post._id, order_json=order_json)
        return post

    def _check_permission(self):
        if self.user_id is g.id:
            raise exceptions.AccessDenied

    def _check_modifiable(self):
        if self.status not in ['recruiting', 'closed']:
            raise Exception

    def _check_join(self):
        if self.status != 'recruiting':
            raise Exception

        if len(self.users) >= self.max_member:
            raise Exception

        if g.id in self.users:
            raise Exception

    def check_quit(self):
        if self.status != 'recruiting':
            raise Exception

        if g.id == self.user_id:
            raise Exception

        if g.id not in self.users:
            raise Exception

    def modify_content(self, order_time, place, min_member, max_member):
        self._check_permission()
        self._check_modifiable()

        title = self.make_title(order_time, self.store.name)
        self.order_time = order_time
        self.title = title
        self.place = place
        self.min_member = min_member
        self.max_member = max_member

    def set_status(self, status):
        self._check_permission()
        self._validate_change_status(status)

        self.status = status

    def _validate_change_status(self, status):
        if status not in ['recruiting', 'closed', 'ordered', 'delivered']:
            raise Exception

        if self.status == 'recruiting':
            if status != 'closed':
                raise Exception

        elif self.status == 'closed':
            if status not in ['recruiting', 'ordered']:
                raise Exception

        elif self.status == 'ordered':
            if status != 'delivered':
                raise Exception

    def join(self, order_json):
        self._check_join()
        post_event.send('joined', store_id=self.store._id, post_id=self._id, order_json=order_json)
        self.users.append(g.id)

    def quit(self):
        self.check_quit()
        post_event.send('quited', post_id=self._id, user_id=g.id)
        self.users.remove(g.id)

    def can_delete(self):
        self._check_permission()
        self._check_modifiable()

    @staticmethod
    def make_title(order_time, store_name):
        return f'[{datetime.fromisoformat(order_time).strftime("%H:%M")}] {store_name}'

    @property
    def json(self):
        return {
            '_id': self._id,
            'store': self.store.json,
            'title': self.title,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'status': self.status,
            'place': self.place,
            'order_time': self.order_time,
            'min_member': self.min_member,
            'max_member': self.max_member,
            'users': self.users
        }
