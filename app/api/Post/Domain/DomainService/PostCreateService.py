from app.api.Post.Domain.Entity.Post import Post
from app.api.Store.Domain.RepositoryInterface import StoreRepository
from flask import g
from bson import ObjectId


class PostCreateService:
    def __init__(self, store_repository: StoreRepository):
        self.store_reader = store_repository

    def create(self, store_id, place, order_time, min_member, max_member):
        store = self.store_reader.find_store(store_id)
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
                    max_member=max_member)

        return post
