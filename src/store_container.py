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

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
    )

    store_repository = providers.Singleton(MongoDBStoreRepository, mongodb_connection)
    menu_repository = providers.Singleton(MongoDBMenuRepository, mongodb_connection)
    menu_dao = providers.Singleton(MongoDBMenuDAO, mongodb_connection)

    store_use_case = providers.Singleton(
        StoreUseCase,
        store_repository=store_repository
    )

    menu_use_case = providers.Singleton(
        MenuUseCase,
        menu_repository=menu_repository,
        menu_dao=menu_dao
    )
