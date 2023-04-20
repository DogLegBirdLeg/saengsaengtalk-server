from app.api.Post.Domain.RepositoryInterface import PostReader
from app.api.Order.Domain.RepositoryInterface import OrderReader


class PostFilteringService:
    def __init__(self, post_reader: PostReader, order_reader: OrderReader):
        self.post_reader = post_reader
        self.order_reader = order_reader

    def filtering(self, option, user_id):
        post_list = self.post_reader.find_post_list()
        post_join_user = self.order_reader.find_post_join_user()

        posts = []
        for post in post_list:
            users = post_join_user[post._id]
            posts.append((post, users))

        if option == 'all':
            return posts

        elif option == 'joinable':
            joinable_post_list = [post for post in posts
                                  if (post[0].recruitment is True)
                                  and (str(user_id) not in post_join_user[post[0]._id])]
            return joinable_post_list

        elif option == 'joined':
            joined_post_list = [post for post in posts
                                if str(user_id) in post_join_user[post[0]._id]]
            return joined_post_list
