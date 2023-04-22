from app.api.Post.Domain.RepositoryInterface import PostRepository
from app.api.Order.Domain.RepositoryInterface import OrderRepository


class PostFilteringService:
    def __init__(self, post_repository: PostRepository, order_repository: OrderRepository):
        self.post_repository = post_repository
        self.order_repository = order_repository

    def filtering(self, option, user_id):
        post_list = self.post_repository.find_post_list()
        post_join_user = self.order_repository.find_post_join_user()

        posts = []
        for post in post_list:
            users = post_join_user[post._id]
            posts.append((post, users))

        if option == 'all':
            return posts

        elif option == 'joinable':
            joinable_post_list = [post for post in posts
                                  if (post[0].status is 'recruiting')
                                  and (str(user_id) not in post_join_user[post[0]._id])]
            return joinable_post_list

        elif option == 'joined':
            joined_post_list = [post for post in posts
                                if str(user_id) in post_join_user[post[0]._id]]
            return joined_post_list
