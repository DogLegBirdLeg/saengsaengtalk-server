from dependency_injector.wiring import inject, Provide
from app.src.container import Container
from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService
from app.api.Order.Domain.RepositoryInterface import OrderRepository

from blinker import signal

post_event = signal('post-event')


@post_event.connect_via('created')
@inject
def post_created_event_handler(sender, store_id, post_id, order_json,
                               order_repository: OrderRepository = Provide[Container.order_repository],
                               order_create_service: OrderCreateService = Provide[Container.order_create_service]):
    order = order_create_service.create(store_id, post_id, order_json)
    order_repository.save(order)


@post_event.connect_via('joined')
@inject
def post_created_event_handler(sender, store_id, post_id, order_json,
                               order_repository: OrderRepository = Provide[Container.order_repository],
                               order_create_service: OrderCreateService = Provide[Container.order_create_service]):
    order = order_create_service.create(store_id, post_id, order_json)
    order_repository.save(order)


@post_event.connect_via('quited')
@inject
def post_created_event_handler(sender, post_id, user_id,
                               order_repository: OrderRepository = Provide[Container.order_repository]):
    order_repository.delete(post_id, user_id)

