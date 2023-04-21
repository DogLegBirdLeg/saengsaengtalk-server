from app.api.Post.Domain.Entity.Post import Post
from app.api.Store.Domain.RepositoryInterface import StoreReader
from flask import g
from bson import ObjectId


class PostCreateService:
    def __init__(self, store_reader: StoreReader):
        self.store_reader = store_reader

    def create(self, store_id, place, order_time, min_member, max_member):


        return post
