from flask_restx import Namespace, Resource
from dependency_injector.wiring import inject, Provide
from app.src.container import Container
from app.api.History.Service.HistoryService import HistoryService
from app.api.Post.Presentation.post import post_model
from app.api.Order.Presentation.order import order_model

history_ns = Namespace('history', description='이전 기록 관련')
history_model = history_ns.inherit('history', post_model, order_model)

@history_ns.route('')
class DeliveryPostHistoryList(Resource):
    @history_ns.doc(security='jwt', description="사용자의 참여 게시글 목록을 반환합니다")
    @history_ns.marshal_list_with(code=200, description='조회 결과', fields=post_model, mask=None)
    @inject
    def get(self, history_service: HistoryService = Provide[Container.history_service]):
        post_history_list = history_service.get_history_list()
        return [post_history.json for post_history in post_history_list]


@history_ns.route('/<string:post_id>')
class DeliveryPostHistoryDetail(Resource):
    @history_ns.doc(security='jwt', description="참여 유저의 주문 목록을 반환합니다")
    @history_ns.marshal_list_with(code=200, description='조회 결과', fields=order_model, mask=None)
    @inject
    def get(self, post_id, history_service: HistoryService = Provide[Container.history_service]):
        orders_history = history_service.get_order_history(post_id)
        return [order_history.json for order_history in orders_history]
