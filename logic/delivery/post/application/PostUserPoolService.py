from logic.delivery.post.application.port.incoming.PostUserPoolUseCase import PostUserPoolUseCase
from logic.delivery.post.application.port.outgoing.persistence.PostUpdateDao import PostUpdateDao
from logic.delivery.post.application.port.outgoing.persistence.PostRepository import PostRepository

import exceptions


class PostUserPoolService(PostUserPoolUseCase):
    def __init__(self, post_repository: PostRepository, post_update_dao: PostUpdateDao):
        self.post_repository = post_repository
        self.post_update_dao = post_update_dao

    def join(self, post_id, user_id, nickname, order_json):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.join(user_id, nickname, order_json)
        self.post_update_dao.update_users(post)

    def quit(self, post_id, user_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.quit(user_id)
        self.post_update_dao.update_users(post)
