from dependency_injector import containers, providers
from redis import StrictRedis
from pymongo import MongoClient
from config.production import redis, mongodb

from app.api.Order.Service.OrderService import OrderService
from app.api.Store.Service.StoreService import StoreService
from app.api.Store.Service.MenuService import MenuService
from app.api.Post.Service.PostService import PostService
from app.api.History.Service.HistoryService import HistoryService

from app.api.Order.Repository.OrderRepository import RedisOrderRepository
from app.api.Post.Repository.PostRepository import RedisPostRepository
from app.api.Store.Repository.StoreRepository import MongoDBStoreRepository
from app.api.Store.Repository.MenuRepository import MongoDBMenuRepository
from app.api.History.Repository.HistoryRepository import MongoDBHistoryRepository

from app.api.Order.Domain.DomainService.OrderCreateService import OrderValidator
from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService
from app.api.Post.Domain.DomainService.PostCreateService import PostCreateService
from app.api.Post.Domain.DomainService.PostFilteringService import PostFilteringService

# auth
from app.auth.Repository.UserRepository import MongoDBUserRepository
from app.auth.Repository.TokenRepository import MongoDBTokenRepository
from app.auth.Service.AuthService import AuthService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.Store.Presentation.store',
                                                            'app.api.Order.Presentation.order',
                                                            'app.api.Post.Presentation.post',
                                                            'app.api.History.Presentation.history',
                                                            'app.auth.Presentation.signin',
                                                            'app.auth.Presentation.signup',
                                                            'app.auth.Presentation.logout'])

    redis_post_connection = providers.Factory(
        StrictRedis,
        host=redis.host,
        port=redis.port,
        password=redis.pwd,
        db=redis.post_db,
        decode_responses=True
    )

    redis_order_connection = providers.Factory(
        StrictRedis,
        host=redis.host,
        port=redis.port,
        password=redis.pwd,
        db=redis.order_db,
        decode_responses=True
    )

    mongoDB_connection = providers.Factory(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
    )

    order_repository = providers.Factory(RedisOrderRepository, redis_order_connection)
    post_repository = providers.Factory(RedisPostRepository, redis_post_connection)
    store_repository = providers.Factory(MongoDBStoreRepository, mongoDB_connection)
    menu_repository = providers.Factory(MongoDBMenuRepository, mongoDB_connection)
    history_repository = providers.Factory(MongoDBHistoryRepository, mongoDB_connection)

    user_repository = providers.Factory(MongoDBUserRepository, mongoDB_connection)
    token_repository = providers.Factory(MongoDBTokenRepository, mongoDB_connection)

    order_validator = providers.Factory(OrderValidator)
    order_create_service = providers.Factory(
        OrderCreateService,
        menu_repository,
        order_validator
    )
    post_create_service = providers.Factory(
        PostCreateService,
        store_repository,
        order_repository
    )

    post_filtering_service = providers.Factory(
        PostFilteringService,
        post_repository,
        order_repository
    )

    order_service = providers.Factory(
        OrderService,
        order_reader=order_repository,
        order_writer=order_repository,
        post_reader=post_repository,
        order_create_service=order_create_service
    )

    post_service = providers.Factory(
        PostService,
        post_reader=post_repository,
        post_writer=post_repository,
        order_reader=order_repository,
        order_writer=order_repository,
        history_writer=history_repository,
        post_filtering_service=post_filtering_service,
        post_create_service=post_create_service,
        order_create_service=order_create_service
    )

    store_service = providers.Factory(
        StoreService,
        store_reader=store_repository
    )

    menu_service = providers.Factory(
        MenuService,
        menu_reader=menu_repository
    )

    history_service = providers.Factory(
        HistoryService,
        history_reader=history_repository
    )

    auth_service = providers.Factory(
        AuthService,
        user_reader=user_repository,
        user_writer=user_repository,
        token_reader=token_repository,
        token_writer=token_repository
    )



