from typing import List
from logic.delivery.post.usecase.IDao import IPostDAO
from logic.delivery.post.usecase.IDao import IStoreDAO
from logic.delivery.post.domain.RepositoryInterface import IPostRepository
from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.domain.dto.PostDto import PostDto

from flask import g
from app import exceptions


class PostUseCaseHelper:
    @staticmethod
    def find_post_by_id(post_repository: IPostRepository, post_id):
        try:
            post = post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        return post


class PostQueryUseCase:
    def __init__(self, post_repository: IPostRepository, post_dao: IPostDAO):
        self.post_repository = post_repository
        self.post_dao = post_dao

    def get_list(self, option) -> List[PostDto]:
        if option == 'joinable':
            posts = self.post_dao.find_joinable_posts_by_user_id(g.id)
            return [PostDto.mapping(post) for post in posts]
        elif option == 'joined':
            posts = self.post_dao.find_joined_posts_by_user_id(g.id)
            return [PostDto.mapping(post) for post in posts]
        elif option == 'all':
            posts = self.post_dao.find_all_posts_by_user_id(g.id)
            return [PostDto.mapping(post) for post in posts]

    def get(self, post_id) -> PostDto:
        post = PostUseCaseHelper.find_post_by_id(self.post_repository, post_id)
        return PostDto.mapping(post)


class PostCreateUseCase:
    def __init__(self, post_repository: IPostRepository, store_dao: IStoreDAO):
        self.post_repository = post_repository
        self.store_dao = store_dao

    def create(self, store_id, place, order_time, min_member, max_member, order_json) -> str:
        try:
            store = self.store_dao.find_store_summary_by_id(store_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistStore

        post = Post.create(g.id, g.nickname, store, place, order_time, min_member, max_member, order_json)

        self.post_repository.save(post)
        return post._id


class PostDeleteUseCase:
    def __init__(self, post_repository: IPostRepository):
        self.post_repository = post_repository

    def delete(self, post_id):
        post = PostUseCaseHelper.find_post_by_id(self.post_repository, post_id)
        post.can_delete(g.id)
        self.post_repository.delete(post._id)


class PostUpdateUseCase:
    def __init__(self, post_repository: IPostRepository, post_dao: IPostDAO):
        self.post_repository = post_repository
        self.post_dao = post_dao

    def modify(self, post_id, order_time, place, min_member, max_member):
        post = PostUseCaseHelper.find_post_by_id(self.post_repository, post_id)
        post.modify_content(g.id, order_time, place, min_member, max_member)
        self.post_dao.update_content(post)

    def change_status(self, post_id, status):
        post = PostUseCaseHelper.find_post_by_id(self.post_repository, post_id)
        post.set_status(g.id, status)
        self.post_dao.update_status(post)

        if status == 'ordered':
            # push 알림 코드
            pass

        elif status == 'delivered':
            # push 알림 코드
            pass


class PostUserPoolUseCase:
    def __init__(self, post_repository: IPostRepository, post_dao: IPostDAO):
        self.post_repository = post_repository
        self.post_dao = post_dao

    def join(self, post_id, order_json):
        post = PostUseCaseHelper.find_post_by_id(self.post_repository, post_id)
        post.join(g.id, g.nickname, order_json)
        self.post_dao.update_users(post)

    def quit(self, post_id):
        post = PostUseCaseHelper.find_post_by_id(self.post_repository, post_id)
        post.quit(g.id)
        self.post_dao.update_users(post)
