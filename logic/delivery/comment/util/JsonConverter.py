from logic.delivery.comment.domain.entity.Comment import Comment


def comment_to_json(comment: Comment):
    return {
        '_id': comment._id,
        'post_id': comment.post_id,
        'create_at': comment.create_at,
        'user_id': comment.user_id,
        'nickname': comment.nickname,
        'status': comment.status,
        'content': comment.content,
        'super_comment_id': comment.super_comment_id
    }