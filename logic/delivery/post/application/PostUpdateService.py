from logic.delivery.post.application.port.incoming.PostUpdateUseCase import PostUpdateUseCase
from logic.delivery.post.application.port.outgoing.persistence.PostRepository import PostRepository
from logic.delivery.post.application.port.outgoing.persistence.PostUpdateDao import PostUpdateDao
from logic.delivery.post.dto.presentation import PostUpdateModel
import exceptions


class PostUpdateService(PostUpdateUseCase):
    def __init__(self, post_repository: PostRepository, post_update_dao: PostUpdateDao):
        self.post_repository = post_repository
        self.post_update_dao = post_update_dao

    def modify(self, user_id, post_id, post_update_model: PostUpdateModel):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.modify_content(user_id=user_id,
                            order_time=post_update_model.order_time,
                            place=post_update_model.place,
                            min_member=post_update_model.min_member,
                            max_member=post_update_model.max_member)
        self.post_update_dao.update_content(post)

    def change_status(self, user_id, post_id, status):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.set_status(user_id, status)
        self.post_update_dao.update_status(post)

    def update_fee(self, user_id, post_id, fee):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.update_fee(user_id, fee)
        self.post_update_dao.update_fee(post)
