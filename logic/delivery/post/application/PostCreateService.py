from logic.delivery.post.application.port.incoming.PostCreateUseCase import PostCreateUseCase
from logic.delivery.post.application.port.outgoing.persistence.PostRepository import PostRepository
from logic.delivery.post.domain.entity.Post import Post


class PostCreateService(PostCreateUseCase):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create(self, user_id, nickname, store_id, place, order_time, min_member, max_member, order_json) -> str:
        post = Post.create(store_id, user_id, nickname, place, order_time, min_member, max_member, order_json)
        self.post_repository.save(post)
        return post._id
