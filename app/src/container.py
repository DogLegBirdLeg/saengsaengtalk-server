from dependency_injector import containers, providers
from redis import StrictRedis
from pymongo import MongoClient
from config.production import redis, mongodb

from app.api.Order.Service.OrderService import OrderService
from app.api.Store.Service.StoreService import StoreService
from app.api.Store.Service.MenuService import MenuService
from app.api.Post.Service.PostService import PostService
from app.api.History.Service.HistoryService import HistoryService

from app.api.Order.infra.OrderRepository import MongoDBOrderRepository
from app.api.Post.Repository.PostRepository import MongoDBPostRepository
from app.api.Store.Repository.StoreRepository import MongoDBStoreRepository
from app.api.Store.Repository.MenuRepository import MongoDBMenuRepository
from app.api.History.Repository.HistoryRepository import MongoDBHistoryRepository
from app.api.Post.Repository.PostDAO import MongoDBPostDAO

from app.api.Order.Domain.DomainService.OrderCreateService import OrderValidator
from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService

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
                                                            'app.auth.Presentation.logout',
                                                            'app.api.Order.Service.PostEventHandler'])

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

    order_repository = providers.Factory(MongoDBOrderRepository, mongoDB_connection)
    post_repository = providers.Factory(MongoDBPostRepository, mongoDB_connection)
    store_repository = providers.Factory(MongoDBStoreRepository, mongoDB_connection)
    menu_repository = providers.Factory(MongoDBMenuRepository, mongoDB_connection)
    history_repository = providers.Factory(MongoDBHistoryRepository, mongoDB_connection)

    post_dao = providers.Factory(MongoDBPostDAO, mongoDB_connection)

    user_repository = providers.Factory(MongoDBUserRepository, mongoDB_connection)
    token_repository = providers.Factory(MongoDBTokenRepository, mongoDB_connection)

    order_validator = providers.Factory(OrderValidator)
    order_create_service = providers.Factory(
        OrderCreateService,
        menu_repository,
        order_validator
    )

    order_service = providers.Factory(
        OrderService,
        order_repository=order_repository,
        post_repository=post_repository,
        order_create_service=order_create_service
    )

    post_service = providers.Factory(
        PostService,
        post_repository=post_repository,
        store_repository=store_repository,
        post_dao=post_dao
    )

    store_service = providers.Factory(
        StoreService,
        store_repository=store_repository
    )

    menu_service = providers.Factory(
        MenuService,
        menu_repository=menu_repository
    )

    history_service = providers.Factory(
        HistoryService,
        history_repository=history_repository
    )

    auth_service = providers.Factory(
        AuthService,
        user_reader=user_repository,
        user_writer=user_repository,
        token_reader=token_repository,
        token_writer=token_repository
    )
