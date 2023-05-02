from flask import request, g
from flask_restx import Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from src.order_container import OrderContainer
from src.post_container import PostContainer
from logic.delivery.order.util.JsonConverter import order_to_json
from logic.delivery.order.application.port.incoming.OrderQueryUseCase import OrderQueryUseCase
from logic.delivery.post.application.port.incoming.PostUserPoolUseCase import PostUserPoolUseCase

order_ns = Namespace('order', description='게시글 주문')

order_line_model = order_ns.model('주문내역', {
    'quantity': fields.Integer(description='개수', example=2),
    'menu': fields.Nested(model=order_ns.model('주문 메뉴', {
        '_id': fields.String(description='메뉴 ID', example='644bb4cc735de5ca8a93c366'),
        'name': fields.String(description='메뉴 이름', example='싱글떡강정세트'),
        'price': fields.Integer(description='메뉴 가격', example=9200),
        'groups': fields.List(fields.Nested(model=order_ns.model('주문 그룹', {
            '_id': fields.String(description='그룹 ID', example='644bb4cc735de5ca8a93c367'),
            'name': fields.String(description='그룹 이름', example='치킨선택'),
            'min_order_quantity': fields.Integer(description='최소 선택 가능', example='1'),
            'max_order_quantity': fields.Integer(description='최대 선택 가능', example='1'),
            'options': fields.List(fields.Nested(model=order_ns.model('주문 옵션', {
                '_id': fields.String(description='옵션 ID', example='644bb4cc735de5ca8a93c368'),
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


@order_ns.route('/<string:post_id>/orders')
class Order(Resource):
    @order_ns.doc(security='jwt', description="모든 주문을 반환합니다")
    @order_ns.marshal_with(code=200, fields=order_ns.model('주문리스트', {
        'orders': fields.List(fields.Nested(model=order_model))
    }), mask=None)
    @inject
    def get(self, post_id, order_use_case: OrderQueryUseCase = Provide[OrderContainer.order_query_service]):
        """게시글 주문 조회"""
        orders = order_use_case.get_list(post_id)

        return {'orders': [order_to_json(order) for order in orders]}

    @order_ns.doc(security='jwt', body=order_model, description="내 주문을 생성합니다")
    @order_ns.response(code=204, description='주문 성공')
    @inject
    def post(self, post_id, post_use_case: PostUserPoolUseCase = Provide[PostContainer.post_user_pool_service]):
        """주문 추가(참여)"""
        data = request.get_json()

        post_use_case.join(post_id, g.id, g.nickname, data)
        return '', 204


@order_ns.route('/<string:post_id>/orders/me')
class MyOrder(Resource):
    @order_ns.doc(security='jwt', description="내 주문을 반환합니다")
    @order_ns.marshal_with(code=200, fields=order_ns.model('주문응답', {
        'order': fields.Nested(model=order_model)
    }), mask=None)
    @inject
    def get(self, post_id, order_use_case: OrderQueryUseCase = Provide[OrderContainer.order_query_service]):
        """내 주문 조회"""
        order = order_use_case.get(post_id)
        return {'order': order_to_json(order)}

    @order_ns.doc(security='jwt', description="내 주문을 삭제합니다")
    @order_ns.response(code=204, description='변경 성공')
    @inject
    def delete(self, post_id, post_use_case: PostUserPoolUseCase = Provide[PostContainer.post_user_pool_service]):
        """주문 삭제(탈퇴)"""
        post_use_case.quit(post_id, g.id)
        return '', 204
