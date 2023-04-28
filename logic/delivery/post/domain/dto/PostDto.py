from typing import List
from logic.delivery.post.domain.vo.store_vo import StoreVO
from logic.delivery.post.domain.entity.Post import Post


class PostDto:
    def __init__(self,
                 _id: str,
                 title: str,
                 store: StoreVO,
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

    @property
    def json(self):
        return {
            '_id': self._id,
            'title': self.title,
            'store': {
                '_id': self.store._id,
                'name': self.store.name,
                'fee': self.store.fee,
                'min_order': self.store.min_order,
                'note': self.store.note
            },
            'user_id': self.user_id,
            'nickname': self.nickname,
            'status': self.status,
            'place': self.place,
            'order_time': self.order_time,
            'min_member': self.min_member,
            'max_member': self.max_member,
            'users': self.users
        }

    @staticmethod
    def mapping(post: Post):
        return PostDto(_id=post._id,
                       title=post.title,
                       store=post.store,
                       user_id=post.user_id,
                       nickname=post.nickname,
                       status=post.status,
                       place=post.place,
                       order_time=post.order_time,
                       min_member=post.min_member,
                       max_member=post.max_member,
                       users=post.users)
