from flask import request
from flask_restx import Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from app.src.container import Container
from app.api.Order.Service.OrderService import OrderService
from app.api.Post.Service.PostService import PostService

order_ns = Namespace('order', description='주문 관련')

order_line_model = order_ns.model('주문내역', {
    'quantity': fields.Integer(description='개수', example=2),
    'menu': fields.Nested(model=order_ns.model('주문 메뉴', {
        '_id': fields.String(description='메뉴 ID', example='6431272e7d80e0f26d3fc3b1'),
        'name': fields.String(description='메뉴 이름', example='싱글떡강정세트'),
        'price': fields.Integer(description='메뉴 가격', example=9200),
        'groups': fields.List(fields.Nested(model=order_ns.model('주문 그룹', {
            '_id': fields.String(description='그룹 ID', example='6431272e7d80e0f26d3fc3b2'),
            'name': fields.String(description='그룹 이름', example='치킨선택'),
            'min_order_quantity': fields.Integer(description='최소 선택 가능', example='1'),
            'max_order_quantity': fields.Integer(description='최대 선택 가능', example='1'),
            'options': fields.List(fields.Nested(model=order_ns.model('주문 옵션', {
                '_id': fields.String(description='옵션 ID', example='6431272e7d80e0f26d3fc3b3'),
                'name': fields.String(description='옵션 이름', example='케이준떡강정(S)'),
                'price': fields.Integer(description='옵션 가격', example=0)
            })))
        })))
    }))
})

order_model = order_ns.model('주문', {
    'user_id': fields.Integer(description='유저 ID', example=1674995732373),
    'nickname': fields.String(description='닉네임', example='개발이'),
    'request_comment': fields.String(description='요청사항', example='피클빼주세요'),
    'order_lines': fields.List(fields.Nested(model=order_line_model))
})


@order_ns.route('/<string:post_id>')
class DeliveryPostOrder(Resource):
    @order_ns.doc(security='jwt', description="모든 주문을 반환합니다")
    @order_ns.marshal_with(code=200, fields=order_ns.model('주문리스트', {
        'orders': fields.List(fields.Nested(model=order_model))
    }), mask=None)
    @inject
    def get(self, post_id, order_service: OrderService = Provide[Container.order_service]):
        orders = order_service.get_list(post_id)
        return {'orders': [order.json for order in orders]}

    @order_ns.doc(security='jwt', body=order_model, description="내 주문을 생성합니다")
    @order_ns.response(code=204, description='주문 성공')
    @inject
    def post(self, post_id, post_service: PostService = Provide[Container.post_service]):
        data = request.get_json()

        post_service.join(post_id, data)
        return '', 204


@order_ns.route('/<string:post_id>/me')
class DeliveryOrderDetail(Resource):
    @order_ns.doc(security='jwt', description="내 주문을 반환합니다")
    @order_ns.marshal_with(code=200, fields=order_ns.model('주문응답', {
        'order': fields.Nested(model=order_model)
    }), mask=None)
    @inject
    def get(self, post_id, order_service: OrderService = Provide[Container.order_service]):
        order = order_service.get(post_id)
        return {'order': order.json}

    @order_ns.doc(security='jwt', description="내 주문을 삭제합니다")
    @order_ns.response(code=204, description='변경 성공')
    @inject
    def delete(self, post_id, post_service: PostService = Provide[Container.post_service]):
        post_service.quit(post_id)
        return '', 204
