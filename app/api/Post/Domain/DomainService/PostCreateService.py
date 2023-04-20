from app.api.Post.Domain.Entity.Post import Post
from app.api.Order.Domain.Entity.Order import Order
from app.api.Store.Domain.RepositoryInterface import StoreReader
from app.api.Order.Domain.RepositoryInterface import OrderWriter


class PostCreateService:
    def __init__(self, store_reader: StoreReader, order_writer: OrderWriter):
        self.store_reader = store_reader
        self.order_writer = order_writer

    def create(self, post_id, store_id, user_id: int, nickname: str, place: str, order_time: str, min_member: int, max_member: int, order: Order):
        store = self.store_reader.find_store(store_id)
        title = Post.make_title(order_time, store.name)
        post = Post(_id=post_id,
                    title=title,
                    store=store,
                    user_id=user_id,
                    nickname=nickname,
                    recruitment=True,
                    place=place,
                    order_time=order_time,
                    min_member=min_member,
                    max_member=max_member)

        self.order_writer.save(post._id, order)

        return post
