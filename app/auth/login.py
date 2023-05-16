from flask import make_response, request
from flask_restx import Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer
from app.util import validator

from logic.user.application.port.incoming.AuthUseCase import AuthUseCase


login_ns = Namespace('login', description='로그인')

signin_format_model = login_ns.model('로그인 포멧', {
    'username': fields.String(description='유저 ID', example='milcampus1234'),
    'pw': fields.String(description='비밀번호', example='dogLegBirdLeg1234'),
    'registration_token': fields.String(description='기기 토큰')
})


@login_ns.route('')
class Login(Resource):
    @login_ns.doc(description="로그인")
    @login_ns.expect(signin_format_model)
    @login_ns.response(code=200, description='로그인 성공', headers={'Authentication': 'access_token/refresh_token'})
    @inject
    def post(self, authentication_use_case: AuthUseCase = Provide[UserContainer.auth_service]):
        """로그인"""
        data = request.get_json()
        username = data['username']
        password = data['pw']
        registration_token = data['registration_token']

        validator.validate_username(username)
        validator.validate_password(password)

        access_token, refresh_token = authentication_use_case.login(username, password, registration_token)

        res = make_response()
        res.headers['Authentication'] = f'{access_token}/{refresh_token}'

        return res
