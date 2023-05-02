from dependency_injector.wiring import inject, Provide
from src.order_container import OrderContainer
from logic.delivery.order.domain.domain_service.OrderCreateService import OrderCreateService
from logic.delivery.order.application.port.outgoing.persistance.OrderRepository import OrderRepository

from blinker import signal

post_event = signal('post-event')


@post_event.connect_via('created')
@inject
def post_created_event_handler(sender, store_id, post_id, user_id, nickname, order_json,
                               order_repository: OrderRepository = Provide[OrderContainer.order_repository],
                               order_create_service: OrderCreateService = Provide[OrderContainer.order_create_service]):

    order = order_create_service.create(store_id, post_id, user_id, nickname, order_json)
    order_repository.save(order)


@post_event.connect_via('joined')
@inject
def post_joined_event_handler(sender, store_id, post_id, user_id, nickname, order_json,
                              order_repository: OrderRepository = Provide[OrderContainer.order_repository],
                              order_create_service: OrderCreateService = Provide[OrderContainer.order_create_service]):
    order = order_create_service.create(store_id, post_id, user_id, nickname, order_json)
    order_repository.save(order)


@post_event.connect_via('quited')
@inject
def post_quited_event_handler(sender, post_id, user_id,
                              order_repository: OrderRepository = Provide[OrderContainer.order_repository]):
    order_repository.delete(post_id, user_id)
