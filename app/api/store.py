from dependency_injector.wiring import inject, Provide
from src.store_container import StoreContainer
from flask_restx import Namespace, Resource, fields

from logic.delivery.store.usecase.StoreUseCase import StoreUseCase
from logic.delivery.store.usecase.MenuUseCase import MenuUseCase

store_ns = Namespace('store', description='가게 정보 관련')

store_model = store_ns.model('가게', {
    '_id': fields.String(description='가게 id', example='6345a45f1c32cd7c4b64d895'),
    'name': fields.String(description='가게 이름', example='맘스터치'),
    'min_order': fields.Integer(description='최소 주문 금액', example=12000),
    'fee': fields.Integer(description='배달비', example=3000)
})
store_detail_model = store_ns.model('가게 상세', {
    '_id': fields.String(description='가게 id', example='6345a45f1c32cd7c4b64d895'),
    'name': fields.String(description='가게 이름', example='맘스터치'),
    'min_order': fields.Integer(description='최소 주문 금액', example=12000),
    'fee': fields.Integer(description='배달비', example=3000),
    'sections': fields.List(fields.Nested(model=store_ns.model('섹션', {
        'section_name': fields.String(description='섹션 이름', example='세트메뉴'),
        'menus': fields.List(fields.Nested(model=store_ns.model('메뉴 요약', {
            '_id': fields.String(description='메뉴 id', example='6345a45f1c32cd7c4b64d896'),
            'name': fields.String(description='메뉴 이름', example='딥치즈버거'),
            'price': fields.Integer(description='메뉴 가격', example=6800)
        })))
    }))),
})
menu_detail_model = store_ns.model('메뉴 상세', {
    '_id': fields.String(description='메뉴 id', example='6345a45f1c32cd7c4b64d896'),
    'name': fields.String(description='메뉴 이름', example='불싸이버거'),
    'price': fields.Integer(description='메뉴 가격', example=10000),
    'groups': fields.List(fields.Nested(model=store_ns.model('그룹 상세', {
        '_id': fields.String(description='그룹 ID', example='63ec9a408ef16d1a09354aa6'),
        'name': fields.String(description='그룹 이름', example='음료변경'),
        'min_order_quantity': fields.Integer(description='최소 선택 개수', example=1),
        'max_order_quantity': fields.Integer(description='최대 선택 개수', example=1),
        'options': fields.List(fields.Nested(store_ns.model('옵션 상세', {
            '_id': fields.String(description='옵션 ID', example='63ec9d6abc985f0d8397a54b'),
            'name': fields.String(description='옵션 이름', example='L콜라'),
            'price': fields.Integer(description='옵션 가격', example=2000)
        })))
    })))
})


@store_ns.route('')
class StoreList(Resource):
    @store_ns.doc(security='jwt', description="가게 목록을 반환합니다")
    @store_ns.marshal_list_with(code=200, description='조회 결과', fields=store_model, mask=None)
    @inject
    def get(self, store_use_case: StoreUseCase = Provide[StoreContainer.store_use_case]):
        stores = store_use_case.get_list()

        return [store.json for store in stores]


@store_ns.route('/<string:store_id>')
class StoreMenuList(Resource):
    @store_ns.doc(security='jwt', params={'store_id': {'description': '가게 ID'}}, description="해당 가게의 상세 정보를 반환합니다")
    @store_ns.marshal_with(code=200, description='조회 결과', fields=store_detail_model, mask=None)
    @inject
    def get(self, store_id, store_use_case: StoreUseCase = Provide[StoreContainer.store_use_case], menu_use_case: MenuUseCase = Provide[StoreContainer.menu_use_case]):

        store = store_use_case.get(store_id)
        sections = menu_use_case.get_summary_list(store_id)

        store_json = store.json
        store_json['sections'] = sections.json

        return store_json


@store_ns.route('/<string:store_id>/<string:menu_id>')
class StoreMenuDetail(Resource):
    @store_ns.doc(security='jwt', description="메뉴의 상세 정보를 반환합니다")
    @store_ns.marshal_with(code=200, description='조회 결과', fields=menu_detail_model, mask=None)
    @inject
    def get(self, store_id, menu_id, menu_use_case: MenuUseCase = Provide[StoreContainer.menu_use_case]):
        menu = menu_use_case.get(menu_id)

        return menu.json
