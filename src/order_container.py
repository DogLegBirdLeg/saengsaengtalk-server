from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from logic.delivery.order.usecase.OrderUseCase import OrderUseCase
from logic.delivery.order.infra.OrderRepository import MongoDBOrderRepository
from logic.delivery.order.domain.domain_service.OrderValidator import OrderValidator
from logic.delivery.order.domain.domain_service.OrderCreateService import OrderCreateService

from logic.delivery.store.infra.MenuRepository import MongoDBMenuRepository


class OrderContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.order',
                                                            'logic.delivery.order.usecase.PostEventHandler'])

    mongodb_connection = providers.Factory(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
    )

    order_repository = providers.Factory(MongoDBOrderRepository, mongodb_connection)
    menu_repository = providers.Factory(MongoDBMenuRepository, mongodb_connection)

    order_use_case = providers.Factory(OrderUseCase, order_repository=order_repository)

    order_validator = providers.Factory(OrderValidator)
    order_create_service = providers.Factory(
        OrderCreateService,
        menu_repository,
        order_validator
    )

