from typing import List
from logic.delivery.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase
from logic.delivery.post.application.port.outgoing.persistence.PostQueryDao import PostQueryDao
from logic.delivery.post.application.port.outgoing.persistence.UserQueryDao import UserQueryDao
from logic.delivery.post.dto.persistance import Post
from app import exceptions


class PostQueryService(PostQueryUseCase):
    def __init__(self, post_query_dao: PostQueryDao, user_query_dao: UserQueryDao):
        self.post_query_dao = post_query_dao
        self.user_query_dao = user_query_dao

    def get_list(self, option, handling_user_id) -> List[Post]:
        if option == 'joinable':
            return self.post_query_dao.find_joinable_posts_by_user_id(handling_user_id)

        elif option == 'joined':
            return self.post_query_dao.find_joined_posts_by_user_id(handling_user_id)

        elif option == 'all':
            return self.post_query_dao.find_all_posts_by_user_id(handling_user_id)

    def get(self, post_id) -> Post:
        try:
            post = self.post_query_dao.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        return post

    def get_owner_user_account_number(self, post_id, handling_user_id):
        try:
            post = self.post_query_dao.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        if handling_user_id not in post.users:
            raise exceptions.AccessDenied

        if post.status not in ['ordered', 'delivered']:
            raise exceptions.BeforeOrdered

        return self.user_query_dao.find_user_account_number(post.user_id)
