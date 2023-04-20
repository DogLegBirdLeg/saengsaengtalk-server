from flask import request
from flask_restx import Resource, Namespace
from app.auth.Service.AuthService import AuthService
from dependency_injector.wiring import inject, Provide
from app.src.container import Container

logout_ns = Namespace('logout', description='로그아웃 API')

parser = logout_ns.parser()
parser.add_argument('Authorization', type=str, location='headers', help='Access Token', required=True)


@logout_ns.route('')
class Logout(Resource):
    @logout_ns.doc(parser=parser, description="로그아웃")
    @logout_ns.response(code=204, description='로그아웃 성공')
    @inject
    def get(self, auth_service: AuthService = Provide[Container.auth_service]):
        access_token = request.headers['Authorization']
        auth_service.logout(access_token)
        return '', 204
