from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb


from logic.delivery.post.usecase.PostUseCase import PostUseCase
from logic.delivery.post.infra.PostRepository import MongoDBPostRepository
from logic.delivery.post.infra.PostDAO import MongoDBPostDAO
from logic.delivery.post.infra.StoreDAO import MongoDBStoreDAO


class PostContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.post',
                                                            'app.api.order'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
    )

    post_repository = providers.Singleton(MongoDBPostRepository, mongodb_connection)
    post_dao = providers.Singleton(MongoDBPostDAO, mongodb_connection)
    store_dao = providers.Singleton(MongoDBStoreDAO, mongodb_connection)

    post_use_case = providers.Singleton(
        PostUseCase,
        post_repository=post_repository,
        store_dao=store_dao,
        post_dao=post_dao
    )
