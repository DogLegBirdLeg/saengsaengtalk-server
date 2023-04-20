from app.api.Store.Domain.Model.Store import Store
from datetime import datetime


class Post:
    def __init__(self,
                 _id: str,
                 title: str,
                 store: Store,
                 user_id: int,
                 nickname: str,
                 recruitment: bool,
                 place: str,
                 order_time: str,
                 min_member: int,
                 max_member: int):
        self._id = _id
        self.title = title
        self.store = store
        self.user_id = user_id
        self.nickname = nickname
        self.recruitment = recruitment
        self.place = place
        self.order_time = order_time
        self.min_member = min_member
        self.max_member = max_member

    def modify_content(self, order_time, place, min_member, max_member):
        title = self.make_title(order_time, self.store.name)
        self.order_time = order_time
        self.title = title
        self.place = place
        self.min_member = min_member
        self.max_member = max_member

    def update_status(self, field, status):
        setattr(self, field, status)

    def is_owner(self, handling_user_id):
        return self.user_id == handling_user_id

    def is_recruit(self):
        return self.recruitment is False

    def is_max_member(self, current_member):
        return current_member >= self.max_member

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
            'recruitment': self.recruitment,
            'place': self.place,
            'order_time': self.order_time,
            'min_member': self.min_member,
            'max_member': self.max_member,
        }
