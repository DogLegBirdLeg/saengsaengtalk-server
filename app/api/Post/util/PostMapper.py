from app.api.Store.util.StoreMapper import StoreMapper
from app.api.Post.Domain.Entity.Post import Post


class PostMapper:
    @staticmethod
    def post_mapping(post_json) -> Post:
        post = Post(post_json['_id'],
                    post_json['title'],
                    StoreMapper.store_mapping(post_json['store']),
                    post_json['user_id'],
                    post_json['nickname'],
                    bool(post_json['recruitment']),
                    post_json['place'],
                    post_json['order_time'],
                    post_json['min_member'],
                    post_json['max_member'])

        return post
