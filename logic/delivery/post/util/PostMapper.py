from logic.delivery.post.domain.vo.store_vo import StoreVO
from logic.delivery.post.domain.entity.Post import Post


class PostMapper:
    @staticmethod
    def post_mapping(post_json) -> Post:
        store_json = post_json['store']
        post = Post(post_json['_id'],
                    post_json['title'],
                    StoreVO(store_json['_id'], store_json['name'], store_json['fee'], store_json['min_order']),
                    post_json['user_id'],
                    post_json['nickname'],
                    post_json['status'],
                    post_json['place'],
                    post_json['order_time'],
                    post_json['min_member'],
                    post_json['max_member'],
                    post_json['users'])

        return post
