from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from logic.delivery.order.application.OrderQueryService import OrderQueryService
from logic.delivery.order.adapter.outgoing.persistance.OrderRepository import MongoDBOrderRepository
from logic.delivery.order.domain.domain_service.OrderValidator import OrderValidator
from logic.delivery.order.domain.domain_service.OrderCreateService import OrderCreateService

from logic.delivery.store.infra.MenuRepository import MongoDBMenuRepository


class OrderContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.order',
                                                            'logic.delivery.order.application.PostEventHandler'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
        connect=False
    )

    order_repository = providers.Singleton(MongoDBOrderRepository, mongodb_connection)
    menu_repository = providers.Singleton(MongoDBMenuRepository, mongodb_connection)

    order_validator = providers.Singleton(OrderValidator)
    order_create_service = providers.Singleton(OrderCreateService, menu_repository, order_validator)
    order_query_service = providers.Singleton(OrderQueryService, order_repository=order_repository)
