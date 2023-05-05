from logic.delivery.post.application.port.incoming.PostCreateUseCase import PostCreateUseCase
from logic.delivery.post.application.port.outgoing.persistence.PostRepository import PostRepository
from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.dto.presentation import PostWriteModel


class PostCreateService(PostCreateUseCase):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create(self, user_id, nickname, post_write_model: PostWriteModel) -> str:
        post = Post.create(store_id=post_write_model.store_id,
                           user_id=user_id,
                           nickname=nickname,
                           place=post_write_model.place,
                           order_time=post_write_model.order_time,
                           min_member=post_write_model.min_member,
                           max_member=post_write_model.max_member,
                           order_json=post_write_model.order)
        self.post_repository.save(post)
        return post._id
