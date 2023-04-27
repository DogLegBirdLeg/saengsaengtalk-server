from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb


from logic.delivery.post.usecase.PostUseCase \
    import PostQueryUseCase, PostCreateUseCase, PostDeleteUseCase, PostUpdateUseCase, PostUserPoolUseCase
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
        connect=False
    )

    post_repository = providers.Singleton(MongoDBPostRepository, mongodb_connection)
    post_dao = providers.Singleton(MongoDBPostDAO, mongodb_connection)
    store_dao = providers.Singleton(MongoDBStoreDAO, mongodb_connection)

    post_query_use_case = providers.Singleton(
        PostQueryUseCase,
        post_repository=post_repository,
        post_dao=post_dao
    )

    post_create_use_case = providers.Singleton(
        PostCreateUseCase,
        post_repository=post_repository,
        store_dao=store_dao
    )

    post_delete_use_case = providers.Singleton(
        PostDeleteUseCase,
        post_repository=post_repository
    )

    post_update_use_case = providers.Singleton(
        PostUpdateUseCase,
        post_repository=post_repository,
        post_dao=post_dao
    )

    post_user_pool_use_case = providers.Singleton(
        PostUserPoolUseCase,
        post_repository=post_repository,
        post_dao=post_dao
    )
