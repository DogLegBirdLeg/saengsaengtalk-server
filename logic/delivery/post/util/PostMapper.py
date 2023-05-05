from logic.delivery.post.domain.entity.Post import Post


class PostMapper:
    @staticmethod
    def post_mapping(post_json) -> Post:
        post = Post(str(post_json['_id']),
                    post_json['store']['_id'],
                    post_json['user_id'],
                    post_json['nickname'],
                    post_json['status'],
                    post_json['place'],
                    post_json['order_time'].strftime('%Y-%m-%dT%H:%M:%S'),
                    post_json['min_member'],
                    post_json['max_member'],
                    post_json['users'])

        return post
