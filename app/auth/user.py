from flask_restx import Resource, Namespace, fields
from app.auth.Service.SignupUseCase import AuthService
from dependency_injector.wiring import inject, Provide
user_ns = Namespace('user', description='유저 관련')

header_parser = user_ns.parser()
header_parser.add_argument('Authorization',
                    type=str,
                    location='headers',
                    help='Access Token',
                    required=True)

user_model = user_ns.model('유저 모델', {
    'id': fields.Integer(description='유저 ID', example=1674995732373),
    'name': fields.String(description='이름', example='김개발'),
    'username': fields.String(description='아이디', example='milcampus1234'),
    'nickname': fields.String(description='닉네임', example='개발이'),
    'account_number': fields.String(description='계좌번호', example='123-1234-123456 농협'),
    'email': fields.String(description='이메일', required=True, example='milcampus1234@naver.com')
})

@user_ns.route('')
class User(Resource):
    @user_ns.doc(parser=header_parser, description='유저 정보를 반환합니다')
    @user_ns.response(code=200, description='조회 성공', model=user_model)
    def get(self):
        #user = AuthService.get_user()
        return ''#user.json
