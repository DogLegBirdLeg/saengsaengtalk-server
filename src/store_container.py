from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb


from logic.delivery.store.usecase.StoreUseCase import StoreUseCase
from logic.delivery.store.usecase.MenuUseCase import MenuUseCase


from logic.delivery.store.infra.StoreRepository import MongoDBStoreRepository
from logic.delivery.store.infra.MenuRepository import MongoDBMenuRepository
from logic.delivery.store.infra.MenuDAO import MongoDBMenuDAO


class StoreContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.store'])

    mongodb_connection = providers.Factory(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
    )

    store_repository = providers.Factory(MongoDBStoreRepository, mongodb_connection)
    menu_repository = providers.Factory(MongoDBMenuRepository, mongodb_connection)
    menu_dao = providers.Factory(MongoDBMenuDAO, mongodb_connection)

    store_use_case = providers.Factory(
        StoreUseCase,
        store_repository=store_repository
    )

    menu_use_case = providers.Factory(
        MenuUseCase,
        menu_repository=menu_repository,
        menu_dao=menu_dao
    )
