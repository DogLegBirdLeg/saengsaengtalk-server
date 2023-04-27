from flask import request
from flask_restx import Resource, Namespace, fields
from logic.user.use_case.SignupUseCase import SignupUseCase, SignupEmailSendUseCase
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer

signup_ns = Namespace('signup', description='회원가입')


signup_format_model = signup_ns.model('회원가입', {
    'auth_code': fields.String(description='인증 코드', example='MiryangCampus2023'),
    'name': fields.String(description='이름', required=True, example='김개발'),
    'username': fields.String(description='유저 ID', required=True, example='milcampus1234'),
    'pw': fields.String(description='비밀번호', required=True, example='dogLegBirdLeg1234'),
    'nickname': fields.String(description='닉네임', required=True, example='개발이'),
    'account_number': fields.String(description='계좌번호', required=True, example='123-1234-123456 농협'),
    'email': fields.String(description='이메일', required=True, example='milcampus1234@naver.com')
})

email_parser = signup_ns.parser()
email_parser.add_argument('email', type=str, help='이메일')


@signup_ns.route('')
class Signup(Resource):
    @signup_ns.doc(parser=email_parser, description="이메일에 인증코드를 발송합니다")
    @signup_ns.response(code=204, description='요청 성공')
    @inject
    def get(self, signup_use_case: SignupEmailSendUseCase = Provide[UserContainer.signup_email_send_use_case]):
        """회원가입 인증코드 발송"""
        email = request.args['email']

        signup_use_case.send_auth_email(email)
        return '', 204

    @signup_ns.doc(description="회원가입")
    @signup_ns.expect(signup_format_model)
    @signup_ns.response(code=201, description='가입 성공')
    @inject
    def post(self, signup_use_case: SignupUseCase = Provide[UserContainer.signup_use_case]):
        """회원가입"""
        data = request.get_json()

        signup_use_case.signup(data['auth_code'], data['name'], data['username'], data['pw'], data['nickname'], data['account_number'], data['email'])

        return '', 201
