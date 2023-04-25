from flask import request
from flask_restx import Resource, Namespace
from logic.auth.use_case.AuthenticationUseCase import JwtAuthenticationUseCase
from dependency_injector.wiring import inject, Provide
from src.auth_container import AuthContainer

logout_ns = Namespace('logout', description='로그아웃 API')

parser = logout_ns.parser()
parser.add_argument('Authorization', type=str, location='headers', help='Access Token', required=True)


@logout_ns.route('')
class Logout(Resource):
    @logout_ns.doc(parser=parser, description="로그아웃")
    @logout_ns.response(code=204, description='로그아웃 성공')
    @inject
    def get(self, authentication_use_case: JwtAuthenticationUseCase = Provide[AuthContainer.authentication_use_case]):
        access_token = request.headers['Authorization']
        authentication_use_case.logout(access_token)
        return '', 204
