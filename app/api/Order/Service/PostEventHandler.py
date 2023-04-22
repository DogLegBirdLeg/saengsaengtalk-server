from dependency_injector.wiring import inject, Provide
from app.src.container import Container
from app.api.History.Domain.RepositoryInterface import HistoryRepository
from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService
from app.api.Order.Domain.RepositoryInterface import OrderRepository

from app.api.Post.Service.PostService import post_ns

post_event = post_ns.signal('post-event')


@post_event.connect_via('created')
@inject
def post_created_event_handler(sender, store_id, post_id, order_json,
                               order_repository: OrderRepository = Provide[Container.order_repository],
                               order_create_service: OrderCreateService = Provide[Container.order_create_service]):
    order = order_create_service.create(store_id, post_id, order_json)
    order_repository.save(post_id, order)


@post_event.connect_via('deleted')
@inject
def post_created_event_handler(sender, post_id,
                               order_repository: OrderRepository = Provide[Container.order_repository],
                               history_repository: HistoryRepository = Provide[Container.history_repository]):
    orders = order_repository.find_order_list_by_post_id(post_id)
    history_repository.save_orders(orders)
    order_repository.delete_post(post_id)


