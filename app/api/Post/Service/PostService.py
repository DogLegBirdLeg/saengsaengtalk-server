from typing import List
from app.api.Store.Domain.RepositoryInterface import StoreRepository
from app.api.Post.Domain.RepositoryInterface import PostRepository
from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Repository.PostDAO import PostDAO

from flask import g


class PostService:
    def __init__(self,
                 post_repository: PostRepository,
                 store_repository: StoreRepository,
                 post_dao: PostDAO):
        self.post_repository = post_repository
        self.store_repository = store_repository
        self.post_dao = post_dao

    def get_list(self, option) -> List[Post]:
        if option == 'all':
            posts = self.post_repository.find_post_list()
            return posts
        elif option == 'joinable':
            posts = self.post_dao.find_joinable_posts(g.id)
            return posts
        elif option == 'joined':
            posts = self.post_dao.find_joined_posts(g.id)
            return posts

    def get(self, post_id) -> Post:
        post = self.post_repository.find_post(post_id)
        return post

    def create(self, store_id, place, order_time, min_member, max_member, order_json) -> str:
        store = self.store_repository.find_store(store_id)
        post = Post.create(store, place, order_time, min_member, max_member, order_json)

        self.post_repository.save(post)
        return post._id

    def delete(self, post_id):
        post = self.post_repository.find_post(post_id)
        post.can_delete()
        self.post_repository.delete(post._id)

    def modify(self, post_id, order_time, place, min_member, max_member):
        post = self.post_repository.find_post(post_id)
        post.modify_content(order_time, place, min_member, max_member)
        self.post_dao.update_content(post)

    def change_status(self, post_id, status):
        post = self.post_repository.find_post(post_id)
        post.set_status(status)
        self.post_dao.update_status(post)
        # TODO: status에 따른 분기처리
        if status == 'ordered':
            # push 알림 코드
            pass

        elif status == 'delivered':
            # push 알림 코드
            pass

    def join(self, post_id, order_json):
        post = self.post_repository.find_post(post_id)
        post.join(order_json)
        self.post_dao.update_users(post)

    def quit(self, post_id):
        post = self.post_repository.find_post(post_id)
        post.quit()
        self.post_dao.update_users(post)
