from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Domain.RepositoryInterface import PostRepository
from app.api.Order.Domain.RepositoryInterface import OrderRepository
from app.api.History.Domain.RepositoryInterface import HistoryRepository


class PostDeleteService:
    def __init__(self,
                 post_repository: PostRepository,
                 order_repository: OrderRepository,
                 history_repository: HistoryRepository):
        self.post_repository = post_repository
        self.order_repository = order_repository
        self.history_repository = history_repository

    def delete(self, post: Post):
        orders = self.order_repository.find_order_list_by_post_id(post._id)
        self.history_repository.save(post, orders)

        self.post_repository.delete(post._id)
        self.order_repository.delete_post(post._id)

