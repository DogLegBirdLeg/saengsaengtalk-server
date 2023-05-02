from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from flask import request, make_response
from src.user_container import UserContainer

from logic.user.application.port.incoming.ForgotUseCase import ForgotUsernameUseCase, ForgotPasswordUseCase


forgot_ns = Namespace('forgot', description='찾기')


auth_code_model = forgot_ns.model('인증 코드', {
    'auth_code': fields.String(description='인증코드', example="4975"),
    'email': fields.String(description='이메일', example='miryany1234@naver.com')
})

email_parser = forgot_ns.parser()
email_parser.add_argument('email', type=str, help='이메일')


@forgot_ns.route('/username')
class ForgotUsername(Resource):
    @forgot_ns.doc(description='이메일로 유저 아이디를 발송합니다', parser=email_parser)
    @forgot_ns.response(code=204, description='조회 성공')
    @inject
    def get(self, forgot_use_case: ForgotUsernameUseCase = Provide[UserContainer.forgot_username_service]):
        """아이디 찾기"""

        email = request.args['email']
        forgot_use_case.send_username_email(email)
        return '', 204


@forgot_ns.route('/password')
class ForgotPassword(Resource):
    @forgot_ns.doc(description='이메일로 비밀번호 찾기 인증 번호를 발송합니다', parser=email_parser)
    @forgot_ns.response(code=204, description='발송 성공')
    @inject
    def get(self, forgot_use_case: ForgotPasswordUseCase = Provide[UserContainer.forgot_password_service]):
        """비밀번호 찾기 인증 메일 발송"""
        email = request.args['email']
        forgot_use_case.send_auth_email(email)
        return '', 204

    @forgot_ns.doc(description='인증번호 비교 후 임시 인가 토큰을 발급합니다')
    @forgot_ns.expect(auth_code_model)
    @forgot_ns.response(code=200, description='인증 성공', headers={'Authentication': 'access_token'})
    @inject
    def post(self, forgot_use_case: ForgotPasswordUseCase = Provide[UserContainer.forgot_password_service]):
        """임시 인가 토큰 발급"""
        data = request.get_json()
        access_token = forgot_use_case.publish_temp_access_token(data['auth_code'], data['email'])
        res = make_response()
        res.headers['Authentication'] = access_token
        return res
