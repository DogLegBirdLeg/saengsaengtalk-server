from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from logic.delivery.post.application.PostCreateService import PostCreateService
from logic.delivery.post.application.PostQueryService import PostQueryService
from logic.delivery.post.application.PostDeleteService import PostDeleteService
from logic.delivery.post.application.PostUpdateService import PostUpdateService
from logic.delivery.post.application.PostUserPoolService import PostUserPoolService

from logic.delivery.post.adapter.outgoing.persistance.PostRepository import MongoDBPostRepository
from logic.delivery.post.adapter.outgoing.persistance.UserQueryAdapter import MongoDBUserQueryDao
from logic.delivery.post.adapter.outgoing.persistance.PostQueryAdapter import MongoDBPostQueryDao
from logic.delivery.post.adapter.outgoing.persistance.PostUpdateAdapter import MongoDBPostUpdateDao


class PostContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.post',
                                                            'app.api.order'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
        connect=False
    )

    post_repository = providers.Singleton(MongoDBPostRepository, mongodb_connection)
    post_query_dao = providers.Singleton(MongoDBPostQueryDao, mongodb_connection)
    post_update_dao = providers.Singleton(MongoDBPostUpdateDao, mongodb_connection)
    user_query_dao = providers.Singleton(MongoDBUserQueryDao, mongodb_connection)

    post_query_service = providers.Singleton(PostQueryService, post_query_dao=post_query_dao, user_query_dao=user_query_dao)
    post_create_service = providers.Singleton(PostCreateService, post_repository=post_repository)
    post_delete_service = providers.Singleton(PostDeleteService, post_repository=post_repository)
    post_update_service = providers.Singleton(PostUpdateService, post_repository=post_repository, post_update_dao=post_update_dao)
    post_user_pool_service = providers.Singleton(PostUserPoolService, post_repository=post_repository, post_update_dao=post_update_dao)
