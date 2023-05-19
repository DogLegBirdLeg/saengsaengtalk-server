from logic.delivery.post.application.port.incoming.PostDeleteUseCase import PostDeleteUseCase
from logic.delivery.post.application.port.outgoing.persistence.PostRepository import PostRepository

import exceptions


class PostDeleteService(PostDeleteUseCase):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def delete(self, post_id, user_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistPost:
            raise exceptions.NotExistPost

        post.can_delete(user_id)
        self.post_repository.delete(post._id)
